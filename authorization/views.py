from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.core.cache import cache
from Crypto.Random import get_random_bytes
# Generate Token Manually

from django.core.cache import cache
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import secrets
from base64 import b64encode, b64decode


def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    # first_name = validated_data.pop('first_name')
    # last_name = validated_data.pop('last_name')
    print(f"user data :--------------------------------->{request.data}, first_name:,----> last name : -->")
    ip_address = request.META.get('REMOTE_ADDR')
    name = f"{request.data['first_name']} {request.data['last_name']}"
    print(name)
    mutable_data = request.data.copy()
    mutable_data['name'] = name
    mutable_data['ip_address'] = ip_address
    print(f"mutable_data:----------------->{mutable_data}")
    serializer = UserRegistrationSerializer(data=mutable_data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    print(email)
    encrypted_password = serializer.data.get('password')
    private_key_pem_tuple = cache.get('private_key')

    user_input_encrypted_password = bytes(b64decode(encrypted_password))
    privateKey = RSA.import_key(private_key_pem_tuple[0])
    salt = cache.get('salt')
    decrypter = PKCS1_OAEP.new(privateKey)
    user_input_plaintext_password_salted = decrypter.decrypt(user_input_encrypted_password)
    password = user_input_plaintext_password_salted[:-len(salt)].decode('utf-8')


    # print(encrypted_password)
    # private_key_pem_tuple = cache.get('private_key')
    # private_key_pem = private_key_pem_tuple[0]
    # print(f"private_key_pem-------> {private_key_pem}")
    # salt = cache.get('salt')
    # print(salt)
    # try:
    #   private_key = RSA.import_key(private_key_pem)
    #   cipher = PKCS1_OAEP.new(private_key)
    # except Exception as e:
    #   print("An error occurred:", str(e))
    # password = cipher.decrypt(encrypted_password.encode('utf-8')).decode('utf-8')
    # print(password)
    # Check if the salt matches to detect possible tampering
    # stored_salt = request.data.get('salt')
    # if salt != stored_salt:
    #     return Response({'error': 'Invalid salt - Possible tampering detected'}, status=status.HTTP_400_BAD_REQUEST)

#     # if employer == "2":
#     salt = "500c1ba19e25a8af7cdf6e2a0e080edcaaa2687b4fcdbe932a0ee95bab0715ad" #cache.get('saltKey')
#     private_key = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4rYoX7lm/HiVxUphsJye\nSBMKhKEnV1PViDTRSkZszYOjNUtkU+lgtRczzECoKbhhmrFLjImURPbN0HqCLBiu\nhynP7vsHH0Nja9wm2386D1S5bZznSXLP3Yw59okj6PrcK2gdoKBmgvqhTDw7Y2Va\nPPqOveNz8KOLZr+e53GJbC1Nt8wdLHHkkt8/7vGfSQWWC10LECbxegEA30KuDYNH\nEdPlSDfPsRsh1xzfd559xiy0L9J5M6sLMUmKqOO7YbM9NepSf9LhkeFEbalFe8jd\n6DecuTEHyadtdmiovNx2Lf1WnF8zEnfXhv0nRCmzUU2IsrvcguAX2tFtHuJvdpgl\nGQIDAQAB\n-----END PUBLIC KEY-----"
# #cache.get('privateKey')
#     # if not private_key:
#     #     User = get_user_model()
#     #     users = User.objects.filter(username=request.user.username).first()
#     #     login_activity = LoginActivity()
#     #     login_activity.ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
#     #     login_activity.user_agent = request.META.get('HTTP_USER_AGENT')
#     #     login_activity.user_id = users.id
#     #     login_activity.app_id = users.app_id
#     #     login_activity.attempt = 'sign-in Failed'
#     #     login_activity.save()
#     #     users.login_attempts = F('login_attempts') + 1
#     #     if users.login_attempts >= 3:
#     #         # Lock the user account
#     #         users.locked = True
#     #         users.save()
#     #         return JsonResponse({'error': 'Your account has been locked.'}, status=429)
#     #     users.save()
#     private_key = serialization.load_pem_private_key(private_key.encode(), password=None, backend=default_backend())
#     decrypted_password = private_key.decrypt(
#         base64.b64decode(encrypted_password),
#         padding.OAEP(
#             mgf=padding.MGF1(algorithm=hashes.SHA256()),
#             algorithm=hashes.SHA256(),
#             label=None
#         )
#     )
#     password = decrypted_password.decode()[:-len(salt)]
#     # Process the password as needed
#     return JsonResponse({'password': password})
#    # return JsonResponse({'error': 'invalid_user'}, status=401)




    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
  
class GenerateKeyPairWithSaltView(APIView):
    # def get(self, request):
    #     # Generate the RSA key pair with a 32-byte random salt
    #     key = RSA.generate(2048)
    #     private_key = key.export_key()
    #     public_key = key.publickey().export_key()
    #     salt = get_random_bytes(32)
    #     encrypted_private_key = None  # Encryption functionality not available in the example code

    #     cache.set('saltKey', salt.hex(), 5)
    #     cache.set('publicKey', public_key.decode(), 5)
    #     cache.set('privateKey', private_key.decode(), 5)

    #     # Return the public key and salt to the client
    #     return JsonResponse({
    #         'publicKey': public_key.decode(),
    #         'salt': salt.hex(),
    #     })
      def get(self, request):
        # Generate an RSA key pair
        key = RSA.generate(2048)
        public_key = key.publickey()
        private_key = key
        salt = secrets.token_urlsafe(16)
        print(salt)
        data = {
            'publicKey': public_key.export_key("PEM").decode("UTF-8"),
            'salt': salt
        }
        privateKey= private_key.export_key("PEM").decode("UTF-8"),
        cache.set('private_key', privateKey, 60)
        cache.set('salt', salt, 60)
        return Response(data, status=status.HTTP_200_OK)

