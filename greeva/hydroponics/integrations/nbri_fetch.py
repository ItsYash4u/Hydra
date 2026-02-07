import hashlib
import json
from datetime import datetime, time
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from django.utils.dateparse import parse_datetime, parse_date, parse_time

from greeva.hydroponics.models_custom import DoserRecord


def _fetch_json(url: str, timeout: int):
    req = Request(url, headers={"User-Agent": "GreevaHydroponics/1.0"})
    with urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", errors="ignore")
    return json.loads(raw)


def map_payload_to_sensors(payload: dict):
    """
    Normalize raw payload into common sensor keys.
    Returns dict with keys: temperature, humidity, ph, ec, co2 (values may be None).
    """
    if not isinstance(payload, dict):
        return {
            "temperature": None,
            "humidity": None,
            "ph": None,
            "ec": None,
            "co2": None,
        }

    lower = {str(k).lower(): v for k, v in payload.items()}

    def pick(keys):
        for key in keys:
            if key in lower and lower[key] not in ("", None):
                return lower[key]
        return None

    temperature = pick(["air_temp", "temperature", "airtemp"])
    ph = pick(["ph", "0"])
    ec = pick(["ec", "1"])
    humidity = pick(["humidity", "hum", "humid", "rh", "1"])
    co2 = pick(["co2"])
    water_temp = pick(["water_temp", "watertemp", "water_temperature", "wtemp"])

    return {
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "ec": ec,
        "co2": co2,
        "water_temp": water_temp,
    }


def _extract_records(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        if isinstance(payload.get("data"), list):
            return payload.get("data")
        if isinstance(payload.get("records"), list):
            return payload.get("records")
        # If dict contains any list, pick the first one
        for value in payload.values():
            if isinstance(value, list):
                return value
        return [payload]
    return []


def _extract_first_record(payload):
    records = _extract_records(payload)
    if records:
        return records[0] if isinstance(records[0], dict) else {"value": records[0]}
    return {}


def _payload_to_array_string(payload):
    try:
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    except Exception:
        return str(payload)


def _compute_source_id(record: dict) -> str:
    for key in ("id", "ID", "Id", "record_id", "Record_ID", "sensor_id", "device_id"):
        value = record.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    if record.get("device_id") and record.get("timestamp"):
        return f"{record.get('device_id')}-{record.get('timestamp')}"
    # Fallback: hash the record
    raw = json.dumps(record, sort_keys=True, separators=(",", ":"))
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


def _parse_source_timestamp(record: dict):
    date_val = record.get("dated") or record.get("date")
    time_val = record.get("timet") or record.get("time")
    if date_val and time_val:
        d = parse_date(str(date_val))
        t = parse_time(str(time_val))
        if d and t:
            return timezone.make_aware(datetime.combine(d, t))

    for key in (
        "timestamp",
        "time",
        "date_time",
        "datetime",
        "created_at",
        "updated_at",
        "date",
    ):
        value = record.get(key)
        if not value:
            continue
        dt = parse_datetime(str(value))
        if dt:
            return dt if timezone.is_aware(dt) else timezone.make_aware(dt)
        d = parse_date(str(value))
        if d:
            return timezone.make_aware(datetime.combine(d, time.min))
    return None


def sync_nbri_records():
    """
    Fetch NBRI doser feed and upsert into local DB.
    Returns tuple: (saved_count, total_records)
    """
    ph_url = getattr(settings, "NBRI_PH_URL", "") or getattr(settings, "NBRI_FETCH_URL", "")
    temp_url = getattr(settings, "NBRI_TEMP_URL", "")
    if not ph_url and not temp_url:
        return (0, 0)

    timeout = int(getattr(settings, "NBRI_FETCH_TIMEOUT", 10))

    ph_payload = _fetch_json(ph_url, timeout) if ph_url else []
    temp_payload = _fetch_json(temp_url, timeout) if temp_url else []

    ph_records = _extract_records(ph_payload)
    temp_records = _extract_records(temp_payload)

    max_len = max(len(ph_records), len(temp_records), 1)
    saved = 0

    for idx in range(max_len):
        ph_item = ph_records[idx] if idx < len(ph_records) else _extract_first_record(ph_payload)
        temp_item = temp_records[idx] if idx < len(temp_records) else _extract_first_record(temp_payload)

        if not isinstance(ph_item, dict):
            ph_item = {"value": ph_item}
        if not isinstance(temp_item, dict):
            temp_item = {" value": temp_item}

        # Rename temp fields to avoid collision
        # pH API has water temperature
        if "temp" in ph_item:
            ph_item["water_temp"] = ph_item.pop("temp")
        if "2" in ph_item:  # temp is also at index "2"
            ph_item["water_temp"] = ph_item.pop("2")
        
        # Temp API has air temperature  
        if "temp" in temp_item:
            temp_item["air_temp"] = temp_item.pop("temp")
        if "0" in temp_item:  # temp is also at index "0"
            temp_item["air_temp"] = temp_item.pop("0")

        combined = {}
        combined.update(ph_item)
        combined.update(temp_item)
        combined["ph_ec_array"] = _payload_to_array_string(ph_payload)
        combined["temp_hum_array"] = _payload_to_array_string(temp_payload)

        source_id = _compute_source_id(combined)
        source_ts = _parse_source_timestamp(combined)
        obj, created = DoserRecord.objects.update_or_create(
            source_id=source_id,
            defaults={
                "payload": combined,
                "source_timestamp": source_ts,
            },
        )
        if created:
            saved += 1

    return (saved, max_len)


def sync_nbri_records_if_stale(cache_key: str = "nbri_last_sync", min_interval_seconds: int = 60):
    """
    Sync the external feed at most once per `min_interval_seconds`.
    Returns the timestamp of the last sync (or None if sync failed).
    """
    try:
        last_sync = cache.get(cache_key)
        now = timezone.now()
        if not last_sync or (now - last_sync).total_seconds() > min_interval_seconds:
            sync_nbri_records()
            cache.set(cache_key, now, min_interval_seconds * 2)
            return now
        return last_sync
    except Exception:
        return cache.get(cache_key)
