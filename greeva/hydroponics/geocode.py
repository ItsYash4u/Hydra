import time
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.core.cache import cache


NOMINATIM_BASE_URL = getattr(settings, "NOMINATIM_BASE_URL", "https://nominatim.openstreetmap.org")
NOMINATIM_USER_AGENT = getattr(settings, "NOMINATIM_USER_AGENT", "GreevaHydroponics/1.0")
NOMINATIM_EMAIL = getattr(settings, "NOMINATIM_EMAIL", None)
NOMINATIM_TIMEOUT = getattr(settings, "NOMINATIM_TIMEOUT", 10)
NOMINATIM_CACHE_TTL = getattr(settings, "NOMINATIM_CACHE_TTL", 86400)


def _throttle():
    last_call = cache.get("nominatim:last_call")
    if last_call:
        delta = time.time() - last_call
        if delta < 1:
            time.sleep(1 - delta)
    cache.set("nominatim:last_call", time.time(), 60)


def _request(path, params):
    if NOMINATIM_EMAIL:
        params["email"] = NOMINATIM_EMAIL
    params["format"] = "json"
    params["addressdetails"] = 1
    params["limit"] = 1

    url = f"{NOMINATIM_BASE_URL}{path}?{urlencode(params)}"
    headers = {"User-Agent": NOMINATIM_USER_AGENT}
    _throttle()
    resp = requests.get(url, headers=headers, timeout=NOMINATIM_TIMEOUT)
    if resp.status_code != 200:
        return None
    return resp.json()


def reverse_geocode(lat, lon):
    cache_key = f"nominatim:reverse:{lat}:{lon}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    data = _request("/reverse", {"lat": lat, "lon": lon})
    if not data:
        return None

    cache.set(cache_key, data, NOMINATIM_CACHE_TTL)
    return data


def forward_geocode(query):
    cache_key = f"nominatim:forward:{query}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    data = _request("/search", {"q": query})
    if not data:
        return None

    cache.set(cache_key, data, NOMINATIM_CACHE_TTL)
    return data
