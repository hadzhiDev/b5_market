from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from accounts.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_login',
        )


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[validate_password])

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'password'
        )
        extra_kwargs = {
            'first_name': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True,)
    new_password = serializers.CharField(required=True, validators=[validate_password])


class SendResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    

class VerifyPasswordResetOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    otp = serializers.CharField(max_length=4)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    otp = serializers.CharField(max_length=4)
    new_password = serializers.CharField(write_only=True, min_length=6)