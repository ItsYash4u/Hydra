from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from greeva.users.auth_helpers import get_current_user

@ensure_csrf_cookie
def custom_login_view(request):
    """Custom login page view - IIT Guwahati branded"""
    if get_current_user(request):
        return redirect('/hydroponics/dashboard/')
    return render(request, 'auth/login_iit.html')

@ensure_csrf_cookie
def custom_signup_view(request):
    """Custom signup page view - IIT Guwahati branded"""
    if get_current_user(request):
        return redirect('/hydroponics/dashboard/')
    return render(request, 'auth/signup_iit.html')


def custom_logout_view(request):
    """Custom logout view that clears session"""
    request.session.flush() # Clears all session data
    return redirect('/')
