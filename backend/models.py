from django.db import models
from django.contrib.auth.models import User

class Hospital(models.Model):
    name = models.CharField(max_length=512)
    parent_hospital = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class User_Role(models.Model):
    USER_ROLES=(
        ('hospital_admin', 'hospital_admin'),
        ('doctor', 'doctor'),
        ('nurse', 'nurse')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_role = models.CharField(max_length=512, choices=USER_ROLES)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - {self.user_role} - {self.hospital}"

class Ward(models.Model):
    name = models.CharField(max_length=512)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    parent_ward = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Device(models.Model):
    name = models.CharField(max_length=512, null=True)
    owner_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    owner_hospital = models.ForeignKey(Hospital, null=True, blank=True, on_delete=models.CASCADE)
    owner_ward = models.ForeignKey(Ward, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Device {self.id} - {self.owner_user} - {self.owner_hospital}"

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    assigned_doctor = models.ForeignKey(User, blank=True, null=True, related_name='patients_assigned', on_delete=models.CASCADE)
    assigned_device = models.ForeignKey(Device, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.assigned_device}"

class VitalData(models.Model):
    VITAL_TYPE_CHOICES=(
        ('blood pressure', 'blood pressure'),
        ('heart beat', 'heart beat'),
        ('body temperature', 'body temperature'),
        ('pulse rate', 'pulse rate')        
    )
    threshold = models.FloatField()
    can_override_threshold = models.BooleanField(default=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    vital_type = models.CharField(max_length=512, choices=VITAL_TYPE_CHOICES)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, blank=True, null=True) 

    def __str__(self):
        return f"{self.patient} - {self.vital_type} - {self.value}"