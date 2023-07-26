from django.contrib import admin
from .models import UserProfile, Hospital, Device, VitalType, VitalData, DevicePermission

admin.site.register(UserProfile)
admin.site.register(Hospital)
admin.site.register(Device)
admin.site.register(VitalType)
admin.site.register(VitalData)
admin.site.register(DevicePermission)