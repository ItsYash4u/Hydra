
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models_custom import Device, UserDevice, SensorValue
from .serializers import SensorValueSerializer, DeviceRegistrationSerializer
from .geocode import reverse_geocode, forward_geocode
from greeva.users.auth_helpers import get_current_user
from django.utils import timezone

class AddDeviceAPIView(APIView):
    permission_classes = [] 

    def post(self, request):
        user = get_current_user(request)
        if not user:
             return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        payload = request.data.copy()

        serializer = DeviceRegistrationSerializer(data=payload, context={'user': user})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            device = serializer.save()
            return Response({
                'message': 'Device added successfully!',
                'device': {
                    'id': device.Device_ID,
                    'device_id': device.Device_ID,
                    'device_name': device.Device_Name or device.Device_ID,
                    'device_type': device.Device_Type,
                    'latitude': device.Latitude,
                    'longitude': device.Longitude
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetDevicesAPIView(APIView):
    permission_classes = [] 

    def get(self, request):
        user = get_current_user(request)
        if not user:
             return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if user.Role == 'admin':
            devices = Device.objects.all()
        else:
            devices = Device.objects.filter(user=user)
        
        device_list = []
        for device in devices:
            try:
                device_sensors = json.loads(device.Device_Sensors) if device.Device_Sensors else []
            except (TypeError, ValueError):
                device_sensors = []
            device_list.append({
                'id': device.Device_ID,
                'device_id': device.Device_ID,
                'device_name': device.Device_Name or f"Unit {device.Device_ID}",
                'name': device.Device_Name or f"Unit {device.Device_ID}",
                'device_type': device.Device_Type,
                'latitude': device.Latitude,
                'longitude': device.Longitude,
                'device_sensors': device_sensors,
                'is_active': True,
                'owner': user.Email_ID 
            })
        
        return Response({'devices': device_list}, status=status.HTTP_200_OK)


class PromoteToAdminAPIView(APIView):
    permission_classes = []

    def post(self, request):
        user = get_current_user(request)
        if not user:
             return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
             
        if user.Role != 'admin':
            return Response({'error': 'Only admins can promote users.'}, status=status.HTTP_403_FORBIDDEN)
        
        user_email = request.data.get('email')
        
        if not user_email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            target_user = UserDevice.objects.get(Email_ID=user_email)
            target_user.Role = 'admin'
            target_user.save()
            return Response({'message': f'{target_user.Email_ID} has been promoted to admin.'}, status=status.HTTP_200_OK)
            
        except UserDevice.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


class ReverseGeocodeAPIView(APIView):
    """
    Resolve latitude/longitude to an address using Nominatim.
    """
    permission_classes = []

    def post(self, request):
        user = get_current_user(request)
        if not user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        lat = request.data.get('latitude')
        lon = request.data.get('longitude')
        if lat is None or lon is None:
            return Response({'error': 'latitude and longitude are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            lat = float(lat)
            lon = float(lon)
        except (TypeError, ValueError):
            return Response({'error': 'Invalid latitude/longitude'}, status=status.HTTP_400_BAD_REQUEST)

        data = reverse_geocode(lat, lon)
        if not data:
            return Response({'error': 'Unable to resolve address'}, status=status.HTTP_400_BAD_REQUEST)

        address = data.get('address', {})
        return Response({
            'display_name': data.get('display_name'),
            'address': {
                'district': address.get('city_district') or address.get('state_district') or address.get('county'),
                'state': address.get('state'),
                'country': address.get('country'),
            },
            'latitude': lat,
            'longitude': lon
        }, status=status.HTTP_200_OK)


class ForwardGeocodeAPIView(APIView):
    """
    Resolve address fields to latitude/longitude using Nominatim.
    """
    permission_classes = []

    def post(self, request):
        user = get_current_user(request)
        if not user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        country = (request.data.get('country') or '').strip()
        state = (request.data.get('state') or '').strip()
        district = (request.data.get('district') or '').strip()
        query = request.data.get('query')

        if not query:
            query = ", ".join([p for p in [district, state, country] if p])

        if not query:
            return Response({'error': 'Address is required'}, status=status.HTTP_400_BAD_REQUEST)

        data = forward_geocode(query)
        if not data:
            return Response({'error': 'Unable to resolve location'}, status=status.HTTP_400_BAD_REQUEST)

        result = data[0]
        try:
            lat = float(result.get('lat'))
            lon = float(result.get('lon'))
        except (TypeError, ValueError):
            return Response({'error': 'Unable to resolve coordinates'}, status=status.HTTP_400_BAD_REQUEST)

        address = result.get('address', {})
        return Response({
            'display_name': result.get('display_name'),
            'address': {
                'district': address.get('city_district') or address.get('state_district') or address.get('county'),
                'state': address.get('state'),
                'country': address.get('country'),
            },
            'latitude': lat,
            'longitude': lon
        }, status=status.HTTP_200_OK)


# ------------------------------------------------------------------------------
# RESTORED SENSOR APIS (Using SensorValue)
# ------------------------------------------------------------------------------

class SensorDataView(APIView):
    """
    GET API: Returns the latest sensor values from SensorValue table.
    """
    permission_classes = [] 

    def get(self, request):
        device_id = request.query_params.get('device_id')
        if not device_id:
             return Response({'error': 'Device ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            device = Device.objects.filter(Device_ID=device_id).first()
            if not device:
                return Response({'error': 'Device not found.'}, status=status.HTTP_404_NOT_FOUND)

            try:
                qs = SensorValue.objects.filter(device_id=device_id).order_by('-timestamp')
                latest = qs.first()
            except Exception:
                latest = (
                    SensorValue.objects
                    .filter(device_id=device_id)
                    .order_by('-date')
                    .first()
                )

            if latest:
                try:
                    selected = set(json.loads(device.Device_Sensors) if device.Device_Sensors else [])
                except (TypeError, ValueError):
                    selected = set()
                if not selected:
                    selected = {'temperature', 'humidity', 'ph', 'ec', 'co2'}

                data = {
                    'temperature': float(latest.temperature) if 'temperature' in selected and latest.temperature is not None else 0,
                    'humidity': float(latest.humidity) if 'humidity' in selected and latest.humidity is not None else 0,
                    'ph': float(latest.pH) if 'ph' in selected and latest.pH is not None else 0,
                    'ec': float(latest.EC) if 'ec' in selected and latest.EC is not None else 0,
                    'co2': float(latest.CO2) if 'co2' in selected and latest.CO2 is not None else 0,
                    'tds': 0,
                    'light': 0,
                    'water_temp': 0,
                    'dissolved_oxygen': 0,
                    'timestamp': latest.timestamp.isoformat() if latest.timestamp else str(latest.date)
                }
                return Response(data)

        except Exception as e:
            print(f"Error in SensorDataView: {e}")
            pass

        return Response({
            'temperature': 0, 'humidity': 0, 'ph': 0, 'ec': 0,
            'light': 0, 'tds': 0, 'co2': 0, 'water_temp': 0,
            'timestamp': None
        })

class SensorHistoryView(APIView):
    """
    GET API: Returns sensor value history for a device (newest first).
    """
    permission_classes = []

    def get(self, request):
        device_id = request.query_params.get('device_id')
        if not device_id:
            return Response({'error': 'Device ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            qs = SensorValue.objects.filter(device_id=device_id).order_by('-timestamp')
            # Trigger evaluation to detect missing column early
            list(qs[:1])
        except Exception:
            qs = SensorValue.objects.filter(device_id=device_id).order_by('-date')
            readings = []
            for idx, sensor_value in enumerate(qs):
                readings.append({
                    'id': idx + 1,
                    'date': sensor_value.date.isoformat() if sensor_value.date else '',
                    'timestamp': sensor_value.timestamp.isoformat() if sensor_value.timestamp else (sensor_value.date.isoformat() if sensor_value.date else ''),
                    'temperature': float(sensor_value.temperature) if sensor_value.temperature is not None else None,
                    'humidity': float(sensor_value.humidity) if sensor_value.humidity is not None else None,
                    'ph': float(sensor_value.pH) if sensor_value.pH is not None else None,
                    'ec': float(sensor_value.EC) if sensor_value.EC is not None else None,
                    'co2': float(sensor_value.CO2) if sensor_value.CO2 is not None else None,
                })

            return Response({
                'device_id': device_id,
                'total_readings': len(readings),
                'readings': readings
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SensorIngestView(APIView):
    """
    POST API: Ingest sensor data into SensorValue.
    """
    permission_classes = [] 

    def post(self, request):
        device_id = request.data.get('device_id')
        if not device_id:
             return Response({'error': 'device_id is required'}, status=status.HTTP_400_BAD_REQUEST)
             
        if not Device.objects.filter(Device_ID=device_id).exists():
              return Response({'error': f'Device {device_id} is not registered.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Auto-map fields from request to models
        # Request keys are likely lowercase (temperature), model is Uppercase (Temperature)
        data = request.data
        
        try:
            SensorValue.objects.create(
                device_id=device_id,
                temperature=data.get('temperature'),
                humidity=data.get('humidity'),
                pH=data.get('ph'),
                EC=data.get('ec'),
                CO2=data.get('co2'),
                date=timezone.now().date()
            )
            return Response({"status": "success", "message": "Data saved to SensorValue"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
