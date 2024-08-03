from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    '''serializer for user model'''
    class Meta:
        model = User
        exclude = ["password", "is_staff", "is_superuser"]