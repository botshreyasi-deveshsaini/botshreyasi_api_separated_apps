from django.urls import path
from .views import SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserProfileView, UserRegistrationView, UserPasswordResetView,GenerateKeyPairWithSaltView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('authenticate/', UserLoginView.as_view(), name='login'),
    path('generate-key-pair/', GenerateKeyPairWithSaltView.as_view(), name='generate-key-pair'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),

]