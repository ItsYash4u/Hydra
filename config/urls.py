# ruff: noqa
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from greeva.users.auth_views import custom_login_view, custom_signup_view, custom_logout_view

urlpatterns = [
    
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("greeva.users.urls", namespace="users")),
    
    # Custom Auth Overrides (Must represent account_login to satisfy default settings)
    path("accounts/login/", custom_login_view, name="account_login"),
    path("accounts/", include("allauth.urls")),

    # Custom Auth Pages (Legacy routes)
    path("auth/login/", custom_login_view, name="custom_login"),
    path("auth/signup/", custom_signup_view, name="custom_signup"),
    path("auth/logout/", custom_logout_view, name="custom_logout"),
    # Hydroponics Management System
    path("hydroponics/", include("greeva.hydroponics.urls", namespace="hydroponics")),
    # API URLs
    path("api/auth/", include("greeva.users.api_urls")),
    path("api/devices/", include("greeva.hydroponics.api_urls")),
    # Your stuff: custom urls includes go here
    path("", include("greeva.pages.urls", namespace="pages")),

    # ...
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
