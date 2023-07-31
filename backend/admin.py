from django.contrib import admin
from .models import User_Role, Hospital, Ward, Patient, Device, VitalData

admin.site.register(User_Role)
admin.site.register(Hospital)
admin.site.register(Ward)
admin.site.register(Patient)
admin.site.register(Device)
admin.site.register(VitalData)