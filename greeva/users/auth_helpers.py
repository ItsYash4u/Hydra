from django.shortcuts import redirect
from functools import wraps
from greeva.hydroponics.models_custom import UserDevice

def custom_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('/auth/login/')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def get_current_user(request):
    """Refetch fresh user object from DB based on session"""
    user_id = request.session.get('user_id')
    if user_id:
        return UserDevice.objects.filter(User_ID=user_id).first()
    return None
