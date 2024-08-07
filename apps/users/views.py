from django.shortcuts import render
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
            return ResponseManager(_type="error", message="invalid email or password!")
        serializer = UserSerializer(user)
        _data = {
            "data":serializer.data,
            "tokens":AuthUtils.generate_tokens(user)
        }
        return ResponseManager(_type="success", message="user successfully authenticated!", data=_data, status_code=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, url_path="register")
    def register(self, request):
        '''registers a user'''
        _data = request.data
        serializer = UserSerializer(data=_data)
        if not serializer.is_valid():
            return ResponseManager(_type="error", message=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return ResponseManager(_type="success", message="user successfully registered!", data=serializer.data, status_code=status.HTTP_201_CREATED)

    @action(methods=["POST"], detail=False, url_path="logout")
    def logout(self, request):
        '''logs a user out'''
        refresh_token = request.data.get("refresh", "")
        if not refresh_token:
            return ResponseManager(
                _type="error",
                message="refresh token must be provided!",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        AuthUtils.blacklist_token(refresh_token)
        return ResponseManager(_type="success", message="user successfully logged out!", status_code=status.HTTP_200_OK)
