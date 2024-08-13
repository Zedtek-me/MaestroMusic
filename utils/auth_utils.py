from apps.users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from typing import Type, Optional, List
from django.db.models import Model

class AuthUtils:
    '''all things related to authentication'''

    @staticmethod
    def authenticate(email, password)->Type[Model]:
        '''authenticates a user'''
        user = User.objects.filter(email=email).first()
        if user is None:
            return None
        if not user.check_password(password):
            return None
        return user


    @staticmethod
    def generate_tokens(user)->dict:
        '''generates tokens for a user'''
        refresh_token = RefreshToken.for_user(user=user)
        return {
            "refresh": str(refresh_token),
            "access": str(refresh_token.access_token),
        }

    @staticmethod
    def blacklist_token(refresh_token_string)->bool:
        '''blacklists a token'''
        refresh_token = RefreshToken(refresh_token_string)
        refresh_token.blacklist()
        return True
