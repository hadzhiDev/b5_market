from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.LoginGenericAPIView.as_view()),
    path('register/', views.RegisterGenericApiView.as_view()),
    path('change-password/', views.ChangePasswordApiView.as_view()),

    path('password-reset/request/', views.RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('password-reset/verify/', views.VerifyPasswordResetOTPView.as_view(), name='verify-password-reset'),
    path('password-reset/complete/', views.ResetPasswordView.as_view(), name='complete-password-reset'),
]