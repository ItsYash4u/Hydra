from django.urls import path
from .views import (
    root_page_view,
    dynamic_pages_view,
    measurement_view,
    services_view,
    analytics_view,
    map_view,
    devices_list_view,
)

app_name = "pages"

urlpatterns = [
    path("", root_page_view, name="root"),
    path("measurement/", measurement_view, name="measurement"),
    path("services/", services_view, name="services"),
    path("analytics/", analytics_view, name="analytics"),
    path("map/", map_view, name="map"),
    path("devices/", devices_list_view, name="devices_list"),
    path("<str:template_name>/", dynamic_pages_view, name="dynamic"),
]
