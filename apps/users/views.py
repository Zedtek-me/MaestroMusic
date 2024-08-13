from django.shortcuts import render
from django.db import transaction
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.users.models import User
from apps.users.serializers import UserSerializer
from utils.auth_utils import AuthUtils
from utils.response_utils import ResponseManager
from django.contrib.auth.models import AnonymousUser
import logging



class AuthFlow(ViewSet):
    '''all things related to user auth'''
    logger = logging.getLogger()
    logger.setLevel("DEBUG")

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

class UserFlow(ViewSet):
    '''all other flows related to the user object'''

    logger = logging.getLogger()
    logger.setLevel("DEBUG")
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(methods=["get"], detail=False, url_path="single_user")
    def get_single_user(self, request):
        '''returns a single user -- logged in or by the give id'''
        user = request.user
        _id = request.query_params.get("user_id")
        if not user or isinstance(user, AnonymousUser):
            user = User.objects.filter(id=_id).first()
        serializer = UserSerializer(user)
        return ResponseManager.handle_response("success", message="user successfully retrieved!", data=serializer.data, status_code=status.HTTP_200_OK)
