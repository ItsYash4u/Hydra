from django.contrib.admin import AdminSite


class HydroponicsAdminSite(AdminSite):
    site_header = "Hydroponics Management System"
    site_title = "Hydroponics Admin"
    index_title = "Hydroponics Management System"

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        return [app for app in app_list if app.get("app_label") == "hydroponics"]


hydroponics_admin_site = HydroponicsAdminSite(name="hydroponics_admin")
