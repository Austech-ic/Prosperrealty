from rest_framework import serializers
from .models import *
from account.serializers import UserSerializer
from django.utils.timezone import now
from admin_dashboard.serializers import ProductReadSerializer

class BookingWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bookings
        exclude=[
            "bookingStatus",
            "initiated_by",
            "stayDuration",
            "confirmationNumber"
        ]
        extra_kwargs={
            "checkInDate":{
                "required":True
            },
            "checkOutDate":{
                "required":True
            },
        }

    def validate(self, attrs):
        checkInDate=attrs["checkInDate"]
        checkOutDate=attrs["checkOutDate"]
        if checkInDate < now().date():
            raise RuntimeError("checkin Date can not be less that Today")

        if checkOutDate < checkInDate:
            raise RuntimeError("checkout Date cant be less than checkin date")
        
        if checkOutDate == checkInDate:
            raise RuntimeError("checkin and check out date must not be equal")
        
        if self.Meta.model.objects.filter(checkInDate__lte=checkOutDate,checkOutDate__gte=checkInDate,product=attrs["product"],bookingStatus="success").exists():
            raise RuntimeError("Product Already Booked between {} and {}".format(checkInDate,checkOutDate))
        
        return super().validate(attrs)


class BookingReadSerializer(serializers.ModelSerializer):
    fullName=serializers.SerializerMethodField()
    email=serializers.SerializerMethodField()
    class Meta:
        model=Bookings
        fields=[
            "id",
            "product",
            "email",
            "fullName",
            "checkInDate",
            "checkOutDate",
            "stayDuration",
            "bookingStatus",
            "confirmationNumber"
        ]

    def get_fullName(self,obj):
        return obj.initiated_by.username
    
    def get_email(self,obj):
        return obj.initiated_by.email


class SingleBookingReadSerializer(serializers.ModelSerializer):
    initiated_by=UserSerializer()
    product=ProductReadSerializer()
    class Meta:
        model=Bookings
        fields="__all__"
        depth=1


class MessageWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Messages
        fields="__all__"


class CommentSerializer(serializers.ModelSerializer):
    createdBy=UserSerializer(read_only=True)
    class Meta:
        model=Comment
        exclude=[
            "blog",
        ]


class AppointmentWriteSerializer(serializers.ModelSerializer):
    userDetail=UserSerializer(read_only=True)
    # propertyName=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Appointment
        exclude=[
            "agentDetail",
            # "userDetail"
        ]
        extra_kwargs={
            "userDetail":{
                "read_only":True
            }
        }

    def validate(self, attrs):
        preferredDate=attrs["preferredDate"]
        if preferredDate < now().date():
            raise RuntimeError("Preferred Date can't be less than today")
        return super().validate(attrs)
    


class SingleAppointmentReadSerializer(serializers.ModelSerializer):
    agentDetail=UserSerializer()
    userDetail=UserSerializer()
    property=ProductReadSerializer()
    class Meta:
        model=Appointment
        fields="__all__"
        
