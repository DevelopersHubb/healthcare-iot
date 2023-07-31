from django.test import TestCase
from django.contrib.auth.models import User
from .models import CustomUser, Hospital, Device, VitalType, VitalData, Patient, Ward
from django.utils import timezone
class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='salman', password='admin')
        self.user_profile = CustomUser.objects.create(user=self.user, user_role='doctor')
    
    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.user, self.user)
        self.assertEqual(self.user_profile.user_role, 'doctor')
        
class HospitalModelTest(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(name='Shoukat Khanum Memorial and Cancer Hospital')
        self.parent_hospital = Hospital.objects.create(name='Parent Hospital')
        self.child_hospital = Hospital.objects.create(name='Child Hospital', parent_hospital=self.parent_hospital)
        
    def test_hospital_creation(self):
        self.assertEqual(self.hospital.name, 'Shoukat Khanum Memorial and Cancer Hospital') 
        self.assertEqual(self.child_hospital.parent_hospital, self.parent_hospital)

class DeviceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='salman', password='admin')
        self.hospital = Hospital.objects.create(name='Shoukat Khanum Memorial and Cancer Hospital')
        self.assigned_user = User.objects.create_user(username='Farukh', password='admin')
        self.assigned_device = Device.objects.create(owner=self.user, hospital=self.hospital, assigned_to=self.assigned_user, is_assigned=True)
    def test_device_creation(self):
        self.assertEqual(self.user.username, 'salman')
        self.assertEqual(self.hospital.name, 'Shoukat Khanum Memorial and Cancer Hospital')
        self.assertEqual(self.assigned_device.assigned_to, self.assigned_user)

class VitalTypeModelTest(TestCase):
    def setUp(self):
        self.vital_type=VitalType.objects.create(name='BP', threshold='160')
    def test_vital_type_creation(self):
        self.assertEqual(self.vital_type.name, 'BP')
        self.assertEqual(self.vital_type.threshold, '160')

class VitalDataModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='salman', password='admin')
        self.hospital = Hospital.objects.create(name='Shoukat Khanum Memorial and Cancer Hospital')
        self.assigned_user = User.objects.create_user(username='Farukh', password='admin')
        self.device=Device.objects.create(owner=self.user, hospital=self.hospital, assigned_to=self.assigned_user, is_assigned=True)
        self.vital_type=VitalType.objects.create(name='Heart Beat', threshold='110')
        self.vital_data=VitalData.objects.create(device=self.device, vital_type=self.vital_type, value='90', timestamp=timezone.now())
    def test_vital_data_creation(self):
        self.assertEqual(self.vital_data.device, self.device)
        self.assertEqual(self.vital_data.vital_type, self.vital_type)
        self.assertEqual(self.vital_data.value, '90')
        
class DevicePermissionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='salman', password='admin')
        self.hospital = Hospital.objects.create(name='Shoukat Khanum Memorial and Cancer Hospital')
        self.assigned_user = User.objects.create_user(username='Farukh', password='admin')
        self.device=Device.objects.create(owner=self.user, hospital=self.hospital, assigned_to=self.assigned_user, is_assigned=True)
        self.device_permission=DevicePermission.objects.create(user=self.user, device=self.device, can_assign=True, can_override_threshold=False, expiry_date='2023-12-31 00:00:00')
        
    def test_device_permission_creation(self):
        self.assertEqual(self.device_permission.user, self.user)
        self.assertEqual(self.device_permission.device, self.device)
        self.assertTrue(self.device_permission.can_assign)
        self.assertEqual(self.device_permission.expiry_date, '2023-12-31 00:00:00')        