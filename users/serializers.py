from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import Patient, Staff, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'password', 'is_patient', 'is_staff', 'is_superadmin')
        extra_kwargs = {'password': {'write_only': True}}

class PatientSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Patient
        fields = ('patient_id', 'user', 'address', 'date_of_birth', 'sex', 'phone_number', 'aadhar_number', 'picture')
        read_only_fields = ('patient_id',)


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'
