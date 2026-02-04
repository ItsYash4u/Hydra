from django.urls import path

from .views import user_detail_view
from .views import user_redirect_view
from .views import user_update_view, user_profile_view
from .auth_views import custom_login_view, custom_signup_view


app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("profile/", view=user_profile_view, name="profile"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
]
