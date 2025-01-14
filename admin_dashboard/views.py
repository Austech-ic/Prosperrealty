import math
from django.shortcuts import render

from utils.app_response import app_response
from utils.error_handler import error_handler
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import (
    JSONParser,
    FormParser,
    MultiPartParser
)
from drf_yasg.openapi import IN_QUERY, Parameter
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction
# Create your views here.


class ProductApiview(APIView):
    parser_classes=[
        JSONParser,
        FormParser,
        MultiPartParser
    ]
    # permission_classes=[
    #     IsAuthenticatedOrReadOnly
    # ]

    @swagger_auto_schema(
            request_body=ProductWriteSerializer
    )
    def post(self,request):
        try:
            with transaction.atomic():
                serializer=ProductWriteSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            return app_response(
                success=True,
                data=serializer.data,
                message="Product created",
                http_status=status.HTTP_201_CREATED
            )      
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )      


    @swagger_auto_schema(
            manual_parameters=[
                Parameter("page", IN_QUERY, type="int", required=False),
                Parameter("limit", IN_QUERY, type="int", required=False),
            ]
    )
    def get(self,request):
        try:
            page=int(request.GET.get("page",0))
            limit=int(request.GET.get("limit",10))
            queryset=Product.objects.select_related(
                # "created_by"
            ).prefetch_related(
                "images","tag"
            ).order_by("-createdAt")
            paginated=queryset[(page * limit) : (page * limit) + limit]
            total_items=queryset.count()
            meta_data={
                "total_page":math.ceil(total_items / limit),
                "current_page":page,
                "per_page":limit,
                "total_items":total_items
            },
            return app_response(
                success=True,
                data=ProductReadSerializer(paginated,many=True).data,
                meta_data=meta_data,
                message="Product fetched",
                http_status=status.HTTP_201_CREATED
            )      
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )  

class SingleProductApiview(APIView):
    parser_classes=[
        JSONParser,
        FormParser,
        MultiPartParser
    ]
    # permission_classes=[
    #     IsAuthenticatedOrReadOnly
    # ]

    @swagger_auto_schema(
            request_body=ProductWriteSerializer
    )
    def put(self,request,product_id):
        try:
            instance=Product.objects.get(id=product_id)
            serializer=ProductWriteSerializer(instance=instance,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return app_response(
                success=True,
                data=serializer.data,
                message="Product created",
                http_status=status.HTTP_201_CREATED
            )      
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )      


    # def get(self,request,product_id):
    #     try:
    #         queryset=Product.objects.select_related(
    #             "created_by"
    #         ).prefetch_related(
    #             "images","tag"
    #         ).get(id=product_id)
    #         return app_response(
    #             success=True,
    #             data=ProductSingleReadSerializer(queryset).data,
    #             message="Product fetched",
    #             http_status=status.HTTP_200_OK
    #         )      
    #     except Exception as e:
    #         return app_response(
    #             success=False,
    #             data=None,
    #             message=error_handler(e),
    #             http_status=status.HTTP_400_BAD_REQUEST
    #         )  


    def delete(self,request,product_id):
        try:
            queryset=Product.objects.get(id=product_id)
            queryset.delete()
            return app_response(
                success=True,
                data=None,
                message="Product deleted",
                http_status=status.HTTP_200_OK
            )      
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )  
        
class ProductTagApiView(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]

    def get(self,request):
        try:
            tags=ProductTag.objects.all()
            return app_response(
                success=True,
                data=ProductTagSerializer(tags,many=True).data,
                message="Product deleted",
                http_status=status.HTTP_200_OK
            )      
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )  
        
class BlogTagApiView(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]

    def get(self,request):
        try:
            tags=BlogTag.objects.all()
            return app_response(
                success=True,
                data=BlogTagSerializer(tags,many=True).data,
                message="Blog Tag Fetched",
                http_status=status.HTTP_200_OK
            )      
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )  
        
class BlogAPiView(APIView):
    parser_classes=[
        JSONParser,
        FormParser,
        MultiPartParser
    ]

    @swagger_auto_schema(
            manual_parameters=[
                Parameter("page", IN_QUERY, type="int", required=False),
                Parameter("limit", IN_QUERY, type="int", required=False),
            ]
    )
    def get(self,request):
        try:
            page=int(request.GET.get("page",0))
            limit=int(request.GET.get("limit",10))
            queryset=Blog.objects.select_related(
                "created_by"
            ).prefetch_related("images").filter(created_by=request.user).order_by("-createdAt")
            paginated=queryset[(page * limit) : (page * limit) + limit]
            total_items=queryset.count()
            meta_data={
                "total_page":math.ceil(total_items / limit),
                "current_page":page,
                "per_page":limit,
                "total_items":total_items
            },
            return app_response(
                success=True,
                data=BlogReadSerializer(paginated,many=True).data,
                message="blog fetched",
                http_status=status.HTTP_200_OK,
                meta_data=meta_data
            )      
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            ) 

    @swagger_auto_schema(
            request_body=WriteBlogSerializer
    )
    def post(self,request):
        try:
            serializer=WriteBlogSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(created_by=request.user)
            return app_response(
                success=True,
                data=serializer.data,
                message="blog created",
                http_status=status.HTTP_201_CREATED
            )    
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            ) 
        
class SingleBlogApiView(APIView):
    parser_classes=[
        JSONParser,
        FormParser,
        MultiPartParser
    ]
    
    def delete(self,request,blog_id):
        try:
            queryset=Blog.objects.get(id=blog_id)
            queryset.delete()
            return app_response(
                success=True,
                data=None,
                message="blog deleted",
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
            request_body=WriteBlogSerializer
    )
    def put(self,request,blog_id):
        try:
            instance=Blog.objects.get(id=blog_id)
            serializer=WriteBlogSerializer(instance=instance,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return app_response(
                success=True,
                data=serializer.data,
                message="Blog updated",
                http_status=status.HTTP_201_CREATED
            )      
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )      