import math
from django.shortcuts import render
from decimal import Decimal
from utils.app_response import app_response
from utils.error_handler import error_handler
from .serializers import *
from .models import *
from admin_dashboard.serializers import (
    ProductReadSerializer,
    ProductSingleReadSerializer,
    BlogReadSerializer,
    SingleBlogReadSerializer,
    StateGetSerializer,
    CountryGetSerializer,
    LocalGovernmentSerializer,
    ProductStatusSerializer,
    ProductTypeSerializer
    )
from admin_dashboard.models import (
    LocalGovt,
    State,
    Country,
    ProductStatus,
    ProductType
)
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
from django.db.models import Q

class ProductApiview(APIView):
    parser_classes=[
        JSONParser,
        FormParser,
        MultiPartParser
    ]
    permission_classes=[
        IsAuthenticatedOrReadOnly
    ]

    @swagger_auto_schema(
            manual_parameters=[
                Parameter("page", IN_QUERY, type="int", required=False),
                Parameter("limit", IN_QUERY, type="int", required=False),
                Parameter("state", IN_QUERY, type="str", required=False),
                Parameter("city", IN_QUERY, type="str", required=False),
                Parameter("property_type", IN_QUERY, type="str", required=False),
                Parameter("high_price", IN_QUERY, type="str", required=False),
                Parameter("low_price", IN_QUERY, type="str", required=False),
                Parameter("search", IN_QUERY, type="str", required=False),
                Parameter("property_status", IN_QUERY, type="str", required=False),

            ]
    )
    def get(self,request):
        try:
            page=int(request.GET.get("page",0))
            limit=int(request.GET.get("limit",10))
            state=request.GET.get("state",None)
            city=request.GET.get("city",None)
            property_type=request.GET.get("property_type",None)
            property_status=request.GET.get("property_status",None)
            high_price=Decimal(request.GET.get("high_price",0.00))
            low_price=Decimal(request.GET.get("low_price",0.00))
            search=request.GET.get("search",None)
            queryset=Product.objects.select_related(
                # "created_by"
            ).prefetch_related(
                "images","tag"
            ).order_by("-createdAt")
            if state:
                queryset=queryset.filter()

            if search:
                queryset=queryset.filter(name__icontains=search)

            if city:
                queryset=queryset.filter()

            if property_type:
                queryset=queryset.filter(productType__name=property_type)

            if property_status:
                queryset=queryset.filter(productStatus__name=property_status)

            if high_price != 0.00:
                queryset=queryset.filter(price__lte=high_price)

            if low_price != 0.00:
                queryset=queryset.filter(price__gte=low_price)

            paginated=queryset[(page * limit) : (page * limit) + limit]
            total_items=queryset.count()
            meta_data={
                "total_page":math.ceil(total_items / limit),
                "current_page":page,
                "per_page":limit,
                "total_items":total_items
            }
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

class BlogAPiView(APIView):
    permission_classes=[
        IsAuthenticatedOrReadOnly
    ]

    @swagger_auto_schema(
            manual_parameters=[
                Parameter("page", IN_QUERY, type="int", required=False),
                Parameter("limit", IN_QUERY, type="int", required=False),
                Parameter("search", IN_QUERY, type="str", required=False),
            ]
    )
    def get(self,request):
        try:
            page=int(request.GET.get("page",0))
            limit=int(request.GET.get("limit",10))
            search=request.GET.get("search",None)
            queryset=Blog.objects.select_related(
                "created_by"
            ).prefetch_related("images").order_by("-createdAt")
            if search:
                queryset=queryset.filter(title__icontains=search)
            paginated=queryset[(page * limit) : (page * limit) + limit]
            total_items=queryset.count()
            meta_data={
                "total_page":math.ceil(total_items / limit),
                "current_page":page,
                "per_page":limit,
                "total_items":total_items
            }
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

class SingleBlogApiview(APIView):
    def get(self,request,blog_id):
        try:
            instance=Blog.objects.select_related(
                "created_by"
            ).prefetch_related("images").get(id=blog_id)
            return app_response(
                success=True,
                data=SingleBlogReadSerializer(instance).data,
                message="blog fetched",
                http_status=status.HTTP_200_OK
            )  
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            ) 
        
class SingleProductApiView(APIView):
    def get(self,request,product_id):
        try:
            queryset=Product.objects.select_related(
                "created_by"
            ).prefetch_related(
                "images","tag"
            ).get(id=product_id)
            return app_response(
                success=True,
                data=ProductSingleReadSerializer(queryset).data,
                message="Product fetched",
                http_status=status.HTTP_200_OK
            )      
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            ) 
        
class ProductBookingApiView(APIView):
    @swagger_auto_schema(
            request_body=BookingWriteSerializer
    )
    def post(self,request):
        try:
            serializer=BookingWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(initiated_by=request.user)
            return app_response(
                success=True,
                data=serializer.data,
                message="Booking Successfull",
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
            manual_parameters=[
                Parameter("page", IN_QUERY, type="int", required=False),
                Parameter("limit", IN_QUERY, type="int", required=False),
            ]
    ) 
    def get(self,request):
        try:
            page=int(request.GET.get("page",0))
            limit=int(request.GET.get("limit",10))
            queryset=Bookings.objects.filter(
                initiated_by=request.user
            ).order_by("-createdAt")
            paginated=queryset[(page * limit) : (page * limit) + limit]
            total_items=queryset.count()
            meta_data={
                "total_page":math.ceil(total_items / limit),
                "current_page":page,
                "per_page":limit,
                "total_items":total_items
            }
            return app_response(
                success=True,
                data=BookingReadSerializer(paginated,many=True).data,
                message="Message Fetched",
                meta_data=meta_data,
                http_status=status.HTTP_200_OK
            )      
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )       
        
class MessageWriteApiView(APIView):
    permission_classes=[

    ]
    def post(self,request):
        try:
            serializer=MessageWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return app_response(
                success=True,
                data=serializer.data,
                message="Message Sent",
                http_status=status.HTTP_200_OK
            )      
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )    
        
class CommentApiView(APIView):
    permission_classes=[

    ]
    def post(self,request,blog_id):
        try:
            blog=Blog.objects.get(id=blog_id)
            serializer=CommentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(blog=blog)
            return app_response(
                success=True,
                data=serializer.data,
                message="Comment saved",
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
            manual_parameters=[
                Parameter("page", IN_QUERY, type="int", required=False),
                Parameter("limit", IN_QUERY, type="int", required=False),
            ]
    )
    def get(self,request,blog_id):
        try:
            page=int(request.GET.get("page",0))
            limit=int(request.GET.get("limit",10))
            blog=Blog.objects.get(id=blog_id)
            queryset=Comment.objects.filter(blog=blog).order_by("-created_at")
            paginated=queryset[(page * limit) : (page * limit) + limit]
            total_items=queryset.count()
            meta_data={
                "total_page":math.ceil(total_items / limit),
                "current_page":page,
                "per_page":limit,
                "total_items":total_items
            }
            return app_response(
                success=True,
                data=CommentSerializer(paginated,many=True).data,
                message="Comment fetched",
                meta_data=meta_data,
                http_status=status.HTTP_200_OK
            )      
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )    
        
class StateApiView(APIView):
    permission_classes=[

    ]
    @swagger_auto_schema(
            manual_parameters=[
                Parameter("country",IN_QUERY,type="str",required=False)
            ]
    )
    def get(self,request):
        try:
            country=request.GET.get("country",None)
            queryset=State.objects.all().order_by("name")
            if country:
                queryset=queryset.filter(country__name=country)
            return app_response(
                success=True,
                data=StateGetSerializer(queryset,many=True).data,
                message="STATE FETCHED SUCCESSFULLY",
                # meta_data=meta_data,
                http_status=status.HTTP_200_OK
            )     
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )  
        
class CountrypiView(APIView):
    permission_classes=[
        
    ]
    def get(self,request):
        try:
            queryset=Country.objects.all().order_by("name")
            return app_response(
                success=True,
                data=CountryGetSerializer(queryset,many=True).data,
                message="COUNTRY FETCHED SUCCESSFULLY",
                # meta_data=meta_data,
                http_status=status.HTTP_200_OK
            )  
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )  
        
class LocalGovernmentApiView(APIView):
    permission_classes=[
        
    ]
    def get(self,request,state_name):
        try:
            queryset=LocalGovt.objects.select_related("state").filter(state__name__iexact=state_name).order_by("LGA")
            return app_response(
                success=True,
                data=LocalGovernmentSerializer(queryset,many=True).data,
                message="STATE FETCHED SUCCESSFULLY",
                # meta_data=meta_data,
                http_status=status.HTTP_200_OK
            ) 
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )  
        
class ProductTypeApiView(APIView):
    permission_classes=[
        
    ]
    def get(self,request):
        try:
            queryset=ProductType.objects.all()
            return app_response(
                success=True,
                data=ProductTypeSerializer(queryset,many=True).data,
                message="STATE FETCHED SUCCESSFULLY",
                # meta_data=meta_data,
                http_status=status.HTTP_200_OK
            ) 
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )  
        
class ProductStatusApiView(APIView):
    permission_classes=[
        
    ]
    def get(self,request):
        try:
            queryset=ProductStatus.objects.all()
            return app_response(
                success=True,
                data=ProductStatusSerializer(queryset,many=True).data,
                message="STATE FETCHED SUCCESSFULLY",
                # meta_data=meta_data,
                http_status=status.HTTP_200_OK
            ) 
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )  

class AppointmentApiView(APIView):
    @swagger_auto_schema(
        request_body=AppointmentWriteSerializer
    )
    def post(self,request):
        try:
            serializer=AppointmentWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            property=serializer.validated_data["property"]
            agent_details=property.created_by
            serializer.save(
                userDetail=request.user,
                agentDetail=agent_details
            )
            return app_response(
                success=True,
                data=None,
                message="APPOINTMENT SUCCESSFUL",
                http_status=status.HTTP_200_OK
            ) 
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )  
        


class ProductBookedDateApiview(APIView):
    class BookedDateSerializer(serializers.ModelSerializer):
        class Meta:
            model=Bookings
            fields=[
                "checkInDate",
                "checkOutDate"
            ]
    permission_classes=[

    ]
    @swagger_auto_schema(
            manual_parameters=[
                Parameter("month", IN_QUERY, type="str", required=False),
                Parameter("year", IN_QUERY, type="str", required=False),
            ]
    )
    def get(self,request,property_id):
        try:
            month = request.GET.get('month',now().date().month)
            year = request.GET.get('year',now().date().year)
            booked_date=Bookings.objects.filter(Q(checkInDate__month=month, checkInDate__year=year) |
                Q(checkOutDate__month=month, checkOutDate__year=year),product__id=property_id,).only("checkInDate","checkOutDate",)
            return app_response(
                success=True,
                data=self.BookedDateSerializer(booked_date,many=True).data,
                message="Booked Date Fetched SUCCESSFUL",
                http_status=status.HTTP_200_OK
            ) 
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )  
