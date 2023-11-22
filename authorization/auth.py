from django.db.models import Q
from django.contrib.auth import get_user_model
# User = get_user_model()
from .models import User
class Auth(object):
    def authenticate(self, creds, password=None, **kwargs):
        try:
            print('Credential =====>',kwargs['email'])
            user = User.objects.get(Q(username=kwargs['email'])|Q(email=kwargs['email']))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            User().set_password(password)