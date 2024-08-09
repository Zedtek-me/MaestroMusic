from django.shortcuts import render
from django.db import transaction
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.users.models import User
from apps.users.serializers import UserSerializer
from utils.auth_utils import AuthUtils
from utils.response_utils import ResponseManager


class AuthFlow(ViewSet):
    '''all things related to user auth'''

    @action(methods=["POST"], detail=False, url_path="login")
    def login(self, request):
        '''logs a user in'''
        email = request.data.get("email")
        password = request.data.get("password")
        user = AuthUtils.authenticate(email, password)
        if user is None:
            return ResponseManager(_type="error", message="invalid email or password!").response
        serializer = UserSerializer(user)
        _data = {
            "data":serializer.data,
            "tokens":AuthUtils.generate_tokens(user)
        }
        return ResponseManager(_type="success", message="user successfully authenticated!", data=_data, status_code=status.HTTP_200_OK).response
    
    @transaction.atomic
    @action(methods=["POST"], detail=False, url_path="register")
    def register(self, request):
        '''registers a user'''
        _data = request.data
        user = User.objects.create_user(**_data)
        user.set_password(_data.get("password", ""))
        user.save()
        serializer = UserSerializer(user)
        _data = {
            "data":serializer.data,
            "tokens":AuthUtils.generate_tokens(user)
        }
        return ResponseManager(_type="success", message="user successfully registered!", data=_data, status_code=status.HTTP_201_CREATED).response
    
    @transaction.atomic
    @action(methods=["POST"], detail=False, url_path="logout")
    def logout(self, request):
        '''logs a user out'''
        refresh_token = request.data.get("refresh", "")
        if not refresh_token:
            return ResponseManager(
                _type="error",
                message="refresh token must be provided!",
                status_code=status.HTTP_400_BAD_REQUEST
            ).response
        AuthUtils.blacklist_token(refresh_token)
        return ResponseManager(_type="success", message="user successfully logged out!", status_code=status.HTTP_200_OK).response
