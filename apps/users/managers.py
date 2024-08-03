from interfaces.managers import BaseManager
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager, BaseManager):
    '''user manager'''

    def create_user(self, **info):
        '''creates a user'''
        if 'email' not in info:
            raise ValidationError(message="email must be provided!")
        user = self.model(email=info.get("email"), **info)
        user.set_password(info.get("password"))
        user.save()
        return user

    def create_superuser(self, **info):
        '''creates a superuser'''
        user = self.create_user(**info)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
