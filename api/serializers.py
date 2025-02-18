from rest_framework import serializers
from .models import User, Patient, HeartRateRecord

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

    def validate_contact_number(self, value):
        # Basic phone number validation
        if not value.replace('+', '').replace('-', '').isdigit():
            raise serializers.ValidationError("Invalid phone number format")
        return value

    def validate_date_of_birth(self, value):
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future")
        return value

class HeartRateRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeartRateRecord
        fields = '__all__' 