from django.urls import path
from .api_views import (
    SignupAPIView, LoginAPIView, VerifyOTPAPIView, ResendOTPAPIView
)

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='api_signup'),
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='api_verify_otp'),
    path('resend-otp/', ResendOTPAPIView.as_view(), name='api_resend_otp'),
]
