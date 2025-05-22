import random

from django.contrib.auth import authenticate
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from .serializers import (LoginSerializer, UserSerializer, RegisterUserSerializer, ChangePasswordSerializer,
                            SendResetPasswordSerializer, VerifyPasswordResetOTPSerializer, ResetPasswordSerializer)
from accounts.models import User, OTPVerification


class LoginGenericAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)
        if user:
            token = Token.objects.get_or_create(user=user)[0]
    
            print(Token.objects.get_or_create(user=user)[0])
            print(Token.objects.get_or_create(user=user)[1])

            user_serializer = UserSerializer(instance=user, context={'request': request})
            return Response({
                **user_serializer.data,
                'token_key': token.key
            })
        return Response({'massage': 'Пользователь не найден или неверный пароль'},
                        status=status.HTTP_400_BAD_REQUEST)
    

class RegisterGenericApiView(GenericAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        
        user_serializer = UserSerializer(instance=user, context={'request': request})
        return Response({
            **user_serializer.data,
            'token': token.key,
        })
    

class ChangePasswordApiView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if self.object.check_password(serializer.data.get("old_password")):
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Пароль успешно обновлен',
                    'data': []
                }
                return Response(response)
            else:
                return Response({"old_password": ['Неверный пароль']}, status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    

class RequestPasswordResetView(GenericAPIView):
    serializer_class = SendResetPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email', None)

        if not email:
            return Response({'message': 'Необходимо указать email'}, status=status.HTTP_400_BAD_REQUEST)

        if email and not User.objects.filter(email=email).exists():
            return Response({'message': 'Пользователь с таким email не найден'}, status=status.HTTP_404_NOT_FOUND)

        otp = str(random.randint(1000, 9999))
        print("Generated OTP:", otp)
        OTPVerification.objects.update_or_create(
            email=email,
            defaults={'otp': otp, 'created_at': now(),}
        )

        message = f"Ваш код для сброса пароля: {otp}"

        response = send_mail(
            subject="Восстановление пароля",
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email], 
        )
        if response == 0:
            return Response({'message': 'Не удалось отправить код на email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        print("Email sent successfully:", response)

        return Response({'message': 'OTP успешно отправлен на email'}, status=status.HTTP_200_OK)

        # return Response({'message': 'Ошибка в методе отправки'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyPasswordResetOTPView(GenericAPIView):
    serializer_class = VerifyPasswordResetOTPSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email', None)
        otp = serializer.validated_data['otp']

        try:
            if email:
                otp_record = OTPVerification.objects.get(email=email, otp=otp,)
            else:
                return Response({'message': 'Необходимо указать email'}, status=status.HTTP_400_BAD_REQUEST)

            if otp_record.is_expired():
                otp_record.delete()
                return Response({'message': 'Срок действия OTP истек'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'OTP успешно проверен'}, status=status.HTTP_200_OK)

        except OTPVerification.DoesNotExist:
            return Response({'message': 'Неверный OTP'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email', None)
        otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']

        try:
            if email:
                otp_record = OTPVerification.objects.get(email=email, otp=otp)
                user = User.objects.get(email=email)
            else:
                return Response({'message': 'Необходимо указать email'}, status=status.HTTP_400_BAD_REQUEST)

            if otp_record.is_expired():
                otp_record.delete()
                return Response({'message': 'Срок действия OTP истек'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            otp_record.delete()

            return Response({'message': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)

        except OTPVerification.DoesNotExist:
            return Response({'message': 'Неверный OTP'}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({'message': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
