from rest_framework import serializers
from .models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util


# move to somewhere else
# not supposed to be in serializers
MAX_FORGET_PASSWORD_ATTEMPTS = 5


class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  # application = serializers.CharField(write_only=True)

  class Meta:
    model = User
    fields= '__all__' #['email', 'name', 'application', 'password', 'password2', 'username']
    extra_kwargs={
      'password':{'write_only':True}
    }

  def create(self, validate_data):
    print(f"validate_data:=====================>{validate_data}")
    return User.objects.create_user(**validate_data)
  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return attrs

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'name']

class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs

# class SendPasswordResetEmailSerializer(serializers.Serializer):
#   email = serializers.EmailField(max_length=255)
#   class Meta:
#     fields = ['email']

#   def validate(self, attrs):
#     email = attrs.get('email')
#     if User.objects.filter(email=email).exists():
#       user = User.objects.get(email = email)
#       uid = urlsafe_base64_encode(force_bytes(user.id))
#       print('Encoded UID', uid)
#       token = PasswordResetTokenGenerator().make_token(user)
#       print('Password Reset Token', token)
#       link = 'http://localhost:8000/api/reset-password/'+uid+'/'+token
#       print('Password Reset Link', link)
#       # Send EMail
#       body = 'Click Following Link to Reset Your Password '+link
#       data = {
#         'subject':'Reset Your Password',
#         'body':body,
#         'to_email':user.email
#       }
#       # Util.send_email(data)
#       return attrs
#     else:
#       raise serializers.ValidationError('You are not a Registered User')

# class UserPasswordResetSerializer(serializers.Serializer):
#   password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
#   password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
#   class Meta:
#     fields = ['password', 'password2']

#   def validate(self, attrs):
#     try:
#       password = attrs.get('password')
#       password2 = attrs.get('password2')
#       uid = self.context.get('uid')
#       token = self.context.get('token')
#       if password != password2:
#         raise serializers.ValidationError("Password and Confirm Password doesn't match")
#       id = smart_str(urlsafe_base64_decode(uid))
#       user = User.objects.get(id=id)
#       if not PasswordResetTokenGenerator().check_token(user, token):
#         raise serializers.ValidationError('Token is not Valid or Expired')
#       user.set_password(password)
#       user.save()
#       return attrs
#     except DjangoUnicodeDecodeError as identifier:
#       PasswordResetTokenGenerator().check_token(user, token)
#       raise serializers.ValidationError('Token is not Valid or Expired')
  
#   class PasswordSerializer(serializers.Serializer):
#     password = serializers.CharField(max_length=512)

class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  # uid = serializers.CharField(max_length=255)
  # token = serializers.CharField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    print(attrs)

    # TODO: We're doing lot of work here(including sending mail) which is not meant
    # for .validate method. Try doing something

    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)

      if user.forget_password_attempts >= MAX_FORGET_PASSWORD_ATTEMPTS:
        user.account_locked = True
        user.save()
        raise serializers.ValidationError("Forgot Password Attempts > {0}".format(MAX_FORGET_PASSWORD_ATTEMPTS))
      elif not user.account_locked:  # <--- this will be retrieved from cache so would be faster.
        user.account_locked = True
        user.save()

      uid = urlsafe_base64_encode(force_bytes(user.id))
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      print('Password Reset Token', token)
      link = 'http://localhost:8000/api/reset-password/'+uid+'/'+token+"/"
      print('Password Reset Link', link)      

      body = 'Click Following Link to Reset Your Password '+link
      emailData = {
        'subject':'Reset Your Password',
        'body':body,
        'to_email':user.email
      }
      print(emailData)

      ######

      from email_log.serializers import EmailLogs_serializer
      from datetime import datetime

      data = dict()
      data['sended_to'] = user.email
      data['message'] = body
      data['sent_date'] = str(datetime.now())
      data['added_by'] = user.id
      # <--- TODO: this is IntegerField in models, supposed to be BooleanField.
      # False would be right value but passing 0 as temporary measure until
      # IntegerField vs BooleanField resolution reached.
      data['is_otp'] = 0

      emailLogs_serializer = EmailLogs_serializer(data=data)

      if emailLogs_serializer.is_valid():
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> data valid")
        emailLogs_serializer.save()
      else:
        print(emailLogs_serializer.errors)
        raise Exception  # <-- TODO: change to some specific exception later

      ######

      # Util.send_email(emailData)
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')
  
  class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=512)
