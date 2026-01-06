from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models_custom import Device, UserDevice
from greeva.users.auth_helpers import get_current_user
import uuid

class AddDeviceAPIView(APIView):
    permission_classes = [] # We handle auth manually

    def post(self, request):
        """
        Add a new device for the logged-in user.
        """
        user = get_current_user(request)
        if not user:
             return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        device_name = request.data.get('device_name') # Not used in model but logic remains
        latitude = request.data.get('latitude', 20.59)
        longitude = request.data.get('longitude', 78.96)
        
        try:
            # Generate unique device ID
            device_id = f"DEV-{uuid.uuid4().hex[:8].upper()}"
            
            # Create device
            device = Device.objects.create(
                User_ID=user.User_ID,
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
        """
        Get all devices for the logged-in user (or all devices if admin).
        """
        user = get_current_user(request)
        if not user:
             return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if user.Role == 'admin':
            devices = Device.objects.all()
        else:
            devices = Device.objects.filter(User_ID=user.User_ID)
        
        device_list = []
        for device in devices:
            device_list.append({
                'id': device.Device_ID,
                'device_id': device.Device_ID,
                'name': f"Unit {device.Device_ID}",
                'latitude': device.Latitude,
                'longitude': device.Longitude,
                'is_active': True,
                'owner': user.Email_ID # Simplified
            })
        
        return Response({'devices': device_list}, status=status.HTTP_200_OK)


class PromoteToAdminAPIView(APIView):
    permission_classes = []

    def post(self, request):
        """
        Promote a user to admin role. Only admins can do this.
        """
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
            
            return Response({
                'message': f'{target_user.Email_ID} has been promoted to admin.'
            }, status=status.HTTP_200_OK)
            
        except UserDevice.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
