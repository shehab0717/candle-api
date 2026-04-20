from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "img"]


class CreateUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=32)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "confirm_password",
            "is_staff",
            "img",
        ]

    def validate(self, data: dict):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords don't match!")
        data.pop("confirm_password")
        return data

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)
