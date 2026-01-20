
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models_custom import Device, UserDevice, SensorValue
from .serializers import SensorValueSerializer
from greeva.users.auth_helpers import get_current_user
import uuid
from django.utils import timezone

class AddDeviceAPIView(APIView):
    permission_classes = [] 

    def post(self, request):
        user = get_current_user(request)
        if not user:
             return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        device_name = request.data.get('device_name') 
        latitude = request.data.get('latitude', 20.59)
        longitude = request.data.get('longitude', 78.96)
        
        device_id = request.data.get('device_id')
        
        try:
            if device_id:
                if Device.objects.filter(Device_ID=device_id).exists():
                    return Response({'error': f'Device ID {device_id} already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                device_id = f"DEV-{uuid.uuid4().hex[:8].upper()}"
            
            device = Device.objects.create(
                user=user,
                Device_ID=device_id,
                Latitude=float(latitude),
                Longitude=float(longitude)
            )
            
            return Response({
                'message': 'Device added successfully!',
                'device': {
                    'id': device.Device_ID,
                    'device_id': device.Device_ID,
                    'name': f"Unit {device.Device_ID}", 
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
            device_list.append({
                'id': device.Device_ID,
                'device_id': device.Device_ID,
                'name': f"Unit {device.Device_ID}",
                'latitude': device.Latitude,
                'longitude': device.Longitude,
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
            # Fetch latest from SensorValue
            qs = SensorValue.objects.filter(device_id=device_id).order_by('-date')
            latest = qs.first()
            
            if latest:
                # Map fields to frontend expectations (lowercase keys)
                data = {
                    'temperature': float(latest.temperature or 0),
                    'humidity': float(latest.humidity or 0),
                    'ph': float(latest.pH or 0),
                    'ec': float(latest.EC or 0),
                    'tds': 0, # Not in SensorValue
                    'co2': 0,
                    'light': 0,
                    'water_temp': 0,
                    'dissolved_oxygen': 0,
                    'timestamp': f"{latest.date}"
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
                date=timezone.now().date()
            )
            return Response({"status": "success", "message": "Data saved to SensorValue"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
