from rest_framework import serializers
from .models import *
from account.serializers import UserSerializer
from django.utils.timezone import now

class BookingWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bookings
        exclude=[
            "bookingStatus",
            "initiated_by",
            "stayDuration"
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
        
        if self.Meta.model.objects.filter(checkInDate__lte=checkOutDate,checkOutDate__gte=checkInDate,product=attrs["product"]).exists():
            raise RuntimeError("Product Already Booked between {} and {}".format(checkInDate,checkOutDate))
        
        return super().validate(attrs)


class BookingReadSerializer(serializers.ModelSerializer):
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
            "bookingStatus"
        ]


class SingleBookingReadSerializer(serializers.ModelSerializer):
    initiated_by=UserSerializer()
    class Meta:
        model=Bookings
        exclude="__all__"
        depth=1


class MessageWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Messages
        fields="__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        exclude=[
            "blog"
        ]


class AppointmentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Appointment
        exclude=[
            "agentDetail",
            "userDetail"
        ]

class SingleAppointmentReadSerializer(serializers.ModelSerializer):
    agentDetail=UserSerializer()
    userDetail=UserSerializer()
    class Meta:
        model=Appointment
        fields="__all__"
        
