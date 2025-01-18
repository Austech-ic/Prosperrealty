import calendar
import math
from django.shortcuts import render
from django.utils.timezone import now
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
from properties.models import (
    Messages,
    Bookings,
    Appointment
)
from properties.serializers import (
    MessageWriteSerializer,
    BookingReadSerializer,
    SingleBookingReadSerializer,
    SingleAppointmentReadSerializer,
    AppointmentWriteSerializer

)
from django.db.models import F, Case, When, Value, FloatField
from .helpers import get_analytics
# Create your views here.


ACCESS_DENIED="ACCESS_DENIED"

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
                if not request.user.is_host():
                    return app_response(
                        success=False,
                        data=None,
                        message=ACCESS_DENIED,
                        http_status=status.HTTP_403_FORBIDDEN
                    )   
                serializer=ProductWriteSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(created_by=request.user)
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
            if not request.user.is_host():
                return app_response(
                    success=False,
                    data=None,
                    message=ACCESS_DENIED,
                    http_status=status.HTTP_403_FORBIDDEN
                )   
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
            if not request.user.is_host():
                return app_response(
                    success=False,
                    data=None,
                    message=ACCESS_DENIED,
                    http_status=status.HTTP_403_FORBIDDEN
                )   
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
            if not request.user.is_host():
                return app_response(
                    success=False,
                    data=None,
                    message=ACCESS_DENIED,
                    http_status=status.HTTP_403_FORBIDDEN
                )   
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
            if not request.user.is_host():
                return app_response(
                    success=False,
                    data=None,
                    message=ACCESS_DENIED,
                    http_status=status.HTTP_403_FORBIDDEN
                )   
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
            if not request.user.is_host():
                return app_response(
                    success=False,
                    data=None,
                    message=ACCESS_DENIED,
                    http_status=status.HTTP_403_FORBIDDEN
                )   
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
            if not request.user.is_host():
                return app_response(
                    success=False,
                    data=None,
                    message=ACCESS_DENIED,
                    http_status=status.HTTP_403_FORBIDDEN
                )   
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
            if not request.user.is_host():
                return app_response(
                    success=False,
                    data=None,
                    message=ACCESS_DENIED,
                    http_status=status.HTTP_403_FORBIDDEN
                )   
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
        
class AllMessageApiView(APIView):

    @swagger_auto_schema(
            manual_parameters=[
                Parameter("page", IN_QUERY, type="int", required=False),
                Parameter("limit", IN_QUERY, type="int", required=False),
            ]
    )
    def get(self,request):
        try:
            if not request.user.is_host():
                return app_response(
                    success=False,
                    data=None,
                    message=ACCESS_DENIED,
                    http_status=status.HTTP_403_FORBIDDEN
                )   
            page=int(request.GET.get("page",0))
            limit=int(request.GET.get("limit",10))
            queryset=Messages.objects.order_by("-createdAt")
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
                data=MessageWriteSerializer(paginated,many=True).data,
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
        
class SingleMessageApiView(APIView):
    def get(self,request,message_id):
        try:
            if not request.user.is_host():
                return app_response(
                    success=False,
                    data=None,
                    message=ACCESS_DENIED,
                    http_status=status.HTTP_403_FORBIDDEN
                )   
            queryset=Messages.objects.get(id=message_id)
            return app_response(
                success=True,
                data=MessageWriteSerializer(queryset).data,
                message="Message Fetched",
                http_status=status.HTTP_200_OK
            )      
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )       
        
    def delete(self,request,message_id):
        try:
            if not request.user.is_host():
                return app_response(
                    success=False,
                    data=None,
                    message=ACCESS_DENIED,
                    http_status=status.HTTP_403_FORBIDDEN
                )   
            queryset=Messages.objects.get(id=message_id)
            queryset.delete()
            return app_response(
                success=True,
                data=None,
                message="Message Deleted",
                http_status=status.HTTP_200_OK
            )      
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )       
        
class BookingsApiview(APIView):
    @swagger_auto_schema(
            manual_parameters=[
                Parameter("page", IN_QUERY, type="int", required=False),
                Parameter("limit", IN_QUERY, type="int", required=False),
            ]
    )
    def get(self,request):
        try:
            if not request.user.is_host():
                return app_response(
                    success=False,
                    data=None,
                    message=ACCESS_DENIED,
                    http_status=status.HTTP_403_FORBIDDEN
                )   
            page=int(request.GET.get("page",0))
            limit=int(request.GET.get("limit",10))
            queryset=Bookings.objects.order_by("-createdAt")
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

class SingleBookingsApiview(APIView):
    class BookingStatusSerializer(serializers.ModelSerializer):
        class Meta:
            model=Bookings
            fields=[
                "bookingStatus"
            ]
    def get(self,request,booking_id):
        try:
            # if not request.user.is_host():
            #     return app_response(
            #         success=False,
            #         data=None,
            #         message=ACCESS_DENIED,
            #         http_status=status.HTTP_403_FORBIDDEN
            #     )   
            queryset=Bookings.objects.get(id=booking_id)
            return app_response(
                success=True,
                data=SingleBookingReadSerializer(queryset).data,
                message="Message Fetched",
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
            request_body=BookingStatusSerializer
    )
    def put(self,request,booking_id):
        try:
            if not request.user.is_host():
                return app_response(
                    success=False,
                    data=None,
                    message=ACCESS_DENIED,
                    http_status=status.HTTP_403_FORBIDDEN
                )   
            queryset=Bookings.objects.get(id=booking_id)
            serializer=self.BookingStatusSerializer(instance=queryset,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return app_response(
                success=True,
                data=None,
                message="Message updated",
                http_status=status.HTTP_200_OK
            )      
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )             
        
    def delete(self,request,booking_id):
        try:
            if not request.user.is_host():
                return app_response(
                    success=False,
                    data=None,
                    message=ACCESS_DENIED,
                    http_status=status.HTTP_403_FORBIDDEN
                )   
            queryset=Bookings.objects.get(id=booking_id)
            queryset.delete()
            return app_response(
                success=True,
                data=None,
                message="Message Deleted",
                http_status=status.HTTP_200_OK
            )      
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )       

class AppointmentAPiView(APIView):
    @swagger_auto_schema(
            manual_parameters=[
                Parameter("page", IN_QUERY, type="int", required=False),
                Parameter("limit", IN_QUERY, type="int", required=False),
            ]
    )
    def get(self,request):
        try:
            if not request.user.is_host():
                return app_response(
                    success=False,
                    data=None,
                    message=ACCESS_DENIED,
                    http_status=status.HTTP_403_FORBIDDEN
                )   
            page=int(request.GET.get("page",0))
            limit=int(request.GET.get("limit",10))
            queryset=Appointment.objects.order_by("-createdAt")
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
                data=AppointmentWriteSerializer(paginated,many=True).data,
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

class SingleAppointmentAPiView(APIView):

    def get(self,request,appointment_id):
        try:
            if not request.user.is_host():
                return app_response(
                    success=False,
                    data=None,
                    message=ACCESS_DENIED,
                    http_status=status.HTTP_403_FORBIDDEN
                )   
            queryset=Appointment.objects.get(id=appointment_id)
            return app_response(
                success=True,
                data=SingleAppointmentReadSerializer(queryset).data,
                message="Message Fetched",
                http_status=status.HTTP_200_OK
            )      
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            ) 
        
        
    def delete(self,request,appointment_id):
        try:
            if not request.user.is_host():
                return app_response(
                    success=False,
                    data=None,
                    message=ACCESS_DENIED,
                    http_status=status.HTTP_403_FORBIDDEN
                )   
            queryset=Appointment.objects.get(id=appointment_id)
            queryset.delete()
            return app_response(
                success=True,
                data=None,
                message="Message Deleted",
                http_status=status.HTTP_200_OK
            )      
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )       

class DashBoardApiView(APIView):
    def get(self,request):
        try:
            if not request.user.is_host():
                return app_response(
                    success=False,
                    data=None,
                    message=ACCESS_DENIED,
                    http_status=status.HTTP_403_FORBIDDEN
                )   
            #Previous month and year logic
            current_date = now()
            current_month = calendar.month_abbr[current_date.month]
            previous_month_number = current_date.month - 1 if current_date.month > 1 else 12
            previous_year = current_date.year if current_date.month > 1 else current_date.year - 1
            previous_month = calendar.month_abbr[previous_month_number]


            totalProperty=Product.objects.count()
            totalAppointment=Appointment.objects.count()
            totalBooking=Bookings.objects.count()
            blog=Blog.objects.select_related("created_by").prefetch_related("comments").order_by("-createdAt")[:3]
    
            visitors = Visitors.objects.annotate(
                is_current_month=Case(
                    When(month=current_month, year=str(current_date.year), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField()
                ),
                is_previous_month=Case(
                    When(month=previous_month, year=str(previous_year), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField()
                )
            )

            # Fetch counts for current and previous months
            current_visitors = visitors.filter(is_current_month=1).first()
            previous_visitors = visitors.filter(is_previous_month=1).first()

            # Extract counts
            current_count = current_visitors.count if current_visitors else 0
            previous_count = previous_visitors.count if previous_visitors else 0

            # Calculate percentage increase
            percentage_increase = ((current_count - previous_count) / previous_count * 100) if previous_count > 0 else 0

            data={
                "visitorCount":current_count,
                "totalBooking":totalBooking,
                "totalProperty":totalProperty,
                "totalAppointment":totalAppointment,
                "percentageIncrease": round(percentage_increase, 2),
                "blog":DashbordBlogReadSerializer(blog,many=True).data,
               
            }
            return app_response(
                success=False,
                data=data,
                message="Details Fetch",
                http_status=status.HTTP_200_OK
            ) 
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            ) 
        

class AnalyticsAPiView(APIView):
    @swagger_auto_schema(
            manual_parameters=[
                Parameter("year", IN_QUERY, type="int", required=False,format="2023"),
            ]
    )
    def get(self,request):
        try:
            if not request.user.is_host():
                return app_response(
                    success=False,
                    data=None,
                    message=ACCESS_DENIED,
                    http_status=status.HTTP_403_FORBIDDEN
                ) 
            today =now()
            year=request.GET.get("year",str(today.year))
            return app_response(
                success=False,
                data=get_analytics(year),
                message="Details Fetch",
                http_status=status.HTTP_200_OK
            ) 
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
            )