from django.db import models
from django.contrib.auth.models import User
    
class UserProfile(models.Model):
    USER_ROLES = (
        ('admin', 'admin'),
        ('doctor', 'doctor'),
        ('nurse', 'nurse'),
        ('patient', 'patient')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_role = models.CharField(max_length=512, choices=USER_ROLES)

    def __str__(self):
        return f"{self.user.username} - {self.user_role}"

class Hospital(models.Model):
    name = models.CharField(max_length=512)
    parent_hospital = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Device(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='assigned_devices')
    is_assigned = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Device {self.id} - {self.owner} - {self.hospital}"

class VitalType(models.Model):
    name = models.CharField(max_length=512)
    threshold = models.FloatField()

    def __str__(self):
        return self.name

class VitalData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    vital_type = models.ForeignKey(VitalType, on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device} - {self.vital_type} - {self.value}"

class DevicePermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    can_assign = models.BooleanField(default=False)
    can_override_threshold = models.BooleanField(default=False)
    expiry_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.device}"