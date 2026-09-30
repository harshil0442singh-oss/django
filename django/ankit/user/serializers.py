import re
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import UserDetails


def validate_name(value):
    if not re.match(r'^[A-Za-z\s]+$', value):
        raise serializers.ValidationError("Enter a valid name")
    return value


def validate_mobile(value):
    if not re.match(r'^\d{10}$', str(value)):
        raise serializers.ValidationError("Enter a valid number")
    return value


def validate_password_strength(value):
    if len(value) < 6:
        raise serializers.ValidationError("Enter a valid password")
    return value


class RecruiterSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.CharField()

    class Meta:
        model = UserDetails
        fields = [
            'name', 'designation', 'company', 'email', 'date_of_birth',
            'gender', 'mobile_number', 'about_company', 'website', 'password'
        ]

    def validate_name(self, value):
        return validate_name(value)

    def validate_email(self, value):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise serializers.ValidationError("Enter a valid email")
        if UserDetails.objects.filter(email=value).exists():
            raise serializers.ValidationError("user details with this email already exists.")
        return value

    def validate_mobile_number(self, value):
        validate_mobile(value)
        if UserDetails.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("user details with this mobile number already exists.")
        return value

    def validate_password(self, value):
        return validate_password_strength(value)

    def create(self, validated_data):
        return UserDetails.objects.create_admin(**validated_data)


class SeekerSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.CharField()

    class Meta:
        model = UserDetails
        fields = [
            'name', 'email', 'date_of_birth', 'gender', 'mobile_number',
            'address', 'password', 'course', 'specialization', 'course_type',
            'college', 'percentage', 'year_of_passing', 'skills', 'summary',
            'experience_level', 'designation', 'responsibilities', 'company',
            'location', 'worked_from', 'to'
        ]

    def validate_name(self, value):
        return validate_name(value)

    def validate_email(self, value):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise serializers.ValidationError("Enter a valid email")
        if UserDetails.objects.filter(email=value).exists():
            raise serializers.ValidationError("user details with this email already exists.")
        return value

    def validate_mobile_number(self, value):
        validate_mobile(value)
        if UserDetails.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("user details with this mobile number already exists.")
        return value

    def validate_password(self, value):
        return validate_password_strength(value)

    def create(self, validated_data):
        return UserDetails.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Unable to authenticate with provided credentials")
        data['user'] = user
        return data


class RecruiterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = [
            'name', 'designation', 'company', 'email', 'date_of_birth',
            'gender', 'mobile_number', 'about_company', 'website'
        ]


class SeekerProfileSerializer(serializers.ModelSerializer):
    percentage = serializers.SerializerMethodField()

    class Meta:
        model = UserDetails
        fields = [
            'name', 'email', 'date_of_birth', 'gender', 'mobile_number',
            'address', 'course', 'specialization', 'course_type', 'college',
            'percentage', 'year_of_passing', 'skills', 'summary',
            'experience_level', 'designation', 'responsibilities', 'company',
            'location', 'worked_from', 'to'
        ]

    def get_percentage(self, obj):
        if obj.percentage is not None:
            return "{:.2f}".format(obj.percentage)
        return None
