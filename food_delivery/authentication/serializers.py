from foodapp.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User=get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['username','password','phone_number','age','email','address']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self,validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number'],
            age=validated_data['age'],
            email=validated_data['email'],
            address=validated_data['address'],
        )
        Token.objects.create(user=user)
        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

