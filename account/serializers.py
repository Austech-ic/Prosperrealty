from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.views import APIView
from drf_extra_fields.fields import Base64ImageField,Base64FileField

class Base64ImagesField(Base64ImageField):
    class Meta:
        swagger_schema_fields = {
            'type': 'String',
            'title': 'Image Content',
            'description': 'Content of the base64 encoded images',
            'read_only': False  # <-- FIX
        }

class AccountCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields=[
            "email",
            "password",
            "confirm_password",
            "username",
            "gender",
            "nationality",
            "address",
            "phoneNumber"

        ]
        extra_kwargs={
            "password":{
                "write_only":True
            },
            "confirm_password":{
                "write_only":True
            }

        }

    def validate(self, attrs):
        if get_user_model().objects.filter(email=attrs['email']).exists():
            raise RuntimeError("Email already exist")
        
        if attrs["password"] != attrs["confirm_password"]:
            raise RuntimeError("Password Doesn't match")
        else:
            return attrs
        
    def create(self, validated_data):
        user=get_user_model().objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.confirm_password=user.password
        user.save()
        return user
     
class UserSerializer(serializers.ModelSerializer):
    image=Base64ImagesField(required=False)
    email=serializers.EmailField(read_only=True)
    role=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=get_user_model()
        fields=[
            "image",
            "email",
            "username",
            "gender",
            "nationality",
            "address",
            "phoneNumber",
            "role"
        ]

    extra_kwargs={
        "email":{
            "read_only":True
        }
    }

    def get_role(self,obj):
        return [role.role for role in obj.role.all()]

class UserWriteSerializer(serializers.ModelSerializer):
    image=Base64ImagesField(required=False)
    email=serializers.EmailField(read_only=True)
    class Meta:
        model=get_user_model()
        fields=[
            "image",
            "email",
            # "password",
            "username",
            "gender",
            "nationality",
            "address",
            "phoneNumber"
        ]

    extra_kwargs={
        "email":{
            "read_only":True
        }
    }

    # def update(self, instance, validated_data):
    #     instance.set_password(validated_data.get("password",instance.password))
    #     return super().update(instance, validated_data)

class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    # default_error_messages = {
    #     "no_active_account": _("No active account found with the given credentials")
    # }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"] = serializers.CharField(
            write_only=True, required=False, allow_null=True
        )

    username_field = get_user_model().USERNAME_FIELD
    email = serializers.EmailField(required=False)

    def validate(self, attrs):
        data = super().validate(attrs)
        
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        res={}
        res["status"]="success"
        res["data"]={
            ** UserSerializer(self.user).data,"token":data}
        res["message"]="USER LOGIN SUCCESSFULLY"
        return res 