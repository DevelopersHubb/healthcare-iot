from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import User_Role, Hospital, Ward, Device, VitalData, Patient


class UserRoleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='salman', password='admin')
        self.hospital = Hospital.objects.create(name='Sheikh Zayed Hospital')
        self.user_role = User_Role.objects.create(user=self.user, user_role='doctor', hospital=self.hospital)

    def test_user_profile_creation(self):
        self.assertEqual(self.user_role.user, self.user)
        self.assertEqual(self.user_role.user_role, 'doctor')
        self.assertEqual(self.user_role.hospital, self.hospital)


class HospitalModelTest(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(name='Shoukat Khanum Memorial and Cancer Hospital')
        self.parent_hospital = Hospital.objects.create(name='Parent Hospital')
        self.child_hospital = Hospital.objects.create(name='Child Hospital', parent_hospital=self.parent_hospital)

    def test_hospital_creation(self):
        self.assertEqual(self.hospital.name, 'Shoukat Khanum Memorial and Cancer Hospital')
        self.assertEqual(self.child_hospital.parent_hospital, self.parent_hospital)


class WardModelTest(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(name='Shoukat Khanum Memorial and Cancer Hospital')
        self.ward = Ward.objects.create(name='testing ward 1', hospital=self.hospital, parent_ward=None)

    def test_hospital_creation(self):
        self.assertEqual(self.ward.name, 'testing ward 1')
        self.assertEqual(self.ward.hospital, self.hospital)
        self.assertIsNone(self.ward.parent_ward)


class DeviceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='salman', password='admin')
        self.hospital = Hospital.objects.create(name='Shoukat Khanum Memorial and Cancer Hospital')
        self.ward = Ward.objects.create(name='test ward 1', hospital=self.hospital)
        self.device = Device.objects.create(
            name='test device',
            owner_user=self.user,
            owner_hospital=self.hospital,
            owner_ward=self.ward
        )

    def test_device_creation(self):
        self.assertEqual(self.device.name, 'test device')
        self.assertEqual(self.device.owner_user, self.user)
        self.assertEqual(self.device.owner_hospital, self.hospital)
        self.assertEqual(self.device.owner_ward, self.ward)


class PatientModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='salman', password='admin')
        self.doctor_user = User.objects.create_user(username='doctor user')
        self.device = Device.objects.create(name='test device')
        self.patient = Patient.objects.create(user=self.user, assigned_device=self.device, assigned_doctor=self.doctor_user)

    def test_patient_creation(self):
        self.assertEqual(self.patient.user, self.user)
        self.assertEqual(self.patient.assigned_device, self.device)
        self.assertEqual(self.patient.assigned_doctor, self.doctor_user)


class VitalDataModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='salman', password='admin')
        self.patient = Patient.objects.create(user=self.user)
        self.device = Device.objects.create(name='test device')

        self.vital_data = VitalData.objects.create(
            threshold='100',
            can_override_threshold=False,
            patient=self.patient,
            vital_type='heart beat',
            value='105',
            timestamp=timezone.now(),
            device=self.device
        )

    def test_vital_data_creation(self):
        self.assertEqual(self.vital_data.threshold, '100')
        self.assertEqual(self.vital_data.patient, self.patient)
        self.assertEqual(self.vital_data.vital_type, 'heart beat')
        self.assertEqual(self.vital_data.value, '105')
        self.assertIsNotNone(self.vital_data.timestamp)
        self.assertEqual(self.vital_data.device, self.device)
