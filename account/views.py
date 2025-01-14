from django.shortcuts import render
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    UserSerializer,
    AccountCreationSerializer,
    TokenObtainPairSerializer,
    UserWriteSerializer
)
from utils.app_response import app_response
from utils.error_handler import error_handler
from rest_framework_simplejwt.views import (TokenObtainPairView)


# Create your views here.
class UserRegistrationApiView(APIView):
    permission_classes=[]

    @swagger_auto_schema(
            request_body=AccountCreationSerializer
    )
    def post(self,request):
        try:
            serializer=AccountCreationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return app_response(
                success=True,
                data=serializer.data,
                message="user created successfully",
                http_status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )
        
class LoginUserAPiView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

class UserProfileApiView(APIView):
    def get(self,request):
        try:
            data=UserSerializer(request.user).data
            return app_response(
                success=True,
                data=data,
                message="PROFILE FETCHED SUCCESSFULLY",
                http_status=status.HTTP_200_OK
            ) 
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            ) 
        

    @swagger_auto_schema(
            request_body=UserWriteSerializer
    )
    def put(self,request):
        try:
            serilaizer=UserWriteSerializer(instance=request.user,data=request.data)
            serilaizer.is_valid(raise_exception=True)
            serilaizer.save()
            return app_response(
                success=True,
                data=serilaizer.data,
                message="PROFILE UPDATED SUCCESSFULLY",
                http_status=status.HTTP_200_OK
            ) 
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )   