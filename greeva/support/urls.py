from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('contact/', views.contact_support_view, name='contact'),
    path('faq/', views.faq_view, name='faq'),
    path('terms/', views.terms_view, name='terms'),
    path('privacy/', views.privacy_view, name='privacy'),
]
