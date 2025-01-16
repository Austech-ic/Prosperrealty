from rest_framework import serializers
from .models import *
from account.serializers import UserSerializer

class BookingWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bookings
        exclude=[
            "bookingStatus",
            # "initiated_by"
        ]


class BookingReadSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bookings
        fields="__all__"
        depth=1

class SingleBookingReadSerializer(serializers.ModelSerializer):
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
        
