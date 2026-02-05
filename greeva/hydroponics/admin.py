
"""
Admin configuration for custom database models
"""

from django import forms
from django.contrib import admin
from django.db.models import F, Window
from django.db.models.functions import RowNumber
from django.utils.html import format_html
from .models import UserDevice, Device, SensorValue
from .admin_site import hydroponics_admin_site


# =========================
# UserDevice Admin
# =========================
@admin.register(UserDevice, site=hydroponics_admin_site)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = (
        'serial_no',
        'user_id_short',
        'full_name',
        'email_id',
        'Role',
        'Phone',
        'Age',
        'Created_At',
    )
    list_display_links = ('serial_no', 'user_id_short')
    list_editable = ('Role',)
    search_fields = ('User_ID', 'Email_ID', 'Name')
    list_filter = ('Role', 'Created_At')
    readonly_fields = ('Created_At', 'Updated_At')
    ordering = ('S_No',)

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        try:
            return qs.annotate(
                row_number=Window(
                    expression=RowNumber(),
                    order_by=F('S_No').asc()
                )
            )
        except Exception:
            return qs

    @admin.display(description="S.No.", ordering="S_No")
    def serial_no(self, obj):
        return getattr(obj, 'row_number', obj.S_No)

    @admin.display(description="User ID", ordering="User_ID")
    def user_id_short(self, obj):
        return obj.User_ID or "-"

    @admin.display(description="Full Name", ordering="Name")
    def full_name(self, obj):
        return obj.Name or "-"

    @admin.display(description="Email ID", ordering="Email_ID")
    def email_id(self, obj):
        return obj.Email_ID


# =========================
# Device Admin
# =========================
@admin.register(Device, site=hydroponics_admin_site)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'Device_ID',
        'Device_Name',
        'Device_Type',
        'user_link',
        'Latitude',
        'Longitude',
        'Created_At',
    )
    list_display_links = ('Device_ID', 'Device_Name')
    search_fields = ('Device_ID', 'Device_Name', 'user__User_ID', 'user__Email_ID')
    list_filter = ('Device_Type', 'Created_At')
    readonly_fields = ('Created_At', 'Updated_At')
    ordering = ('-Created_At',)

    @admin.display(description="User (Owner)", ordering="user__User_ID")
    def user_link(self, obj):
        if not obj.user_id:
            return "-"
        url = f"/admin/hydroponics/userdevice/{obj.user_id}/change/"
        return format_html('<a href="{}">{}</a>', url, obj.user_id)


@admin.register(SensorValue, site=hydroponics_admin_site)
class SensorValueAdmin(admin.ModelAdmin):
    class SensorValueForm(forms.ModelForm):
        device_id = forms.ChoiceField(label="Device id", required=False)

        class Meta:
            model = SensorValue
            fields = "__all__"

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            device_choices = [(d.Device_ID, d.Device_ID) for d in Device.objects.all().order_by('Device_ID')]
            self.fields['device_id'].choices = [('', '---------')] + device_choices

    form = SensorValueForm

    list_display = (
        'device_id',
        'date',
        'temperature',
        'humidity',
        'pH',
        'EC',
        'CO2',
    )
    search_fields = ("device_id",)
    list_filter = ("date",)
    ordering = ('-date',)

    fieldsets = (
        ('Device Information', {
            'fields': ('device_id', 'date')
        }),
        ('Sensor Readings', {
            'fields': ('temperature', 'humidity', 'pH', 'EC', 'CO2')
        }),
    )
