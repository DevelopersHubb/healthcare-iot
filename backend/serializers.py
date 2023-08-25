from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Hospital, Patient, Device, User_Role


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Role
        fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class CustomCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    user_role = serializers.ChoiceField(choices=User_Role.USER_ROLES)
    hospital_name = serializers.CharField(max_length=255)
    device_name = serializers.CharField(max_length=255)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        hospital = Hospital.objects.create(
            name=validated_data['hospital_name']
        )

        Patient.objects.create(user=user)

        Device.objects.create(
            name=validated_data['device_name'],
            owner_user=user,
            owner_hospital=hospital
        )

        return validated_data

    def update(self, instance, validated_data):
        user = instance['user']
        hospital = instance['hospital']
        device = instance['device']

        user.email = validated_data.get('email', user.email)
        user.user_role = validated_data.get('user_role', user.user_role)
        user.save()

        hospital.name = validated_data.get('hospital_name', hospital.name)
        hospital.save()

        device.name = validated_data.get('device_name', device.name)
        device.save()

        return instance

    def validate_password(self, value):
        if len(value) > 11:
            raise serializers.ValidationError('Password cannot be more than 8 digits')
        return value
