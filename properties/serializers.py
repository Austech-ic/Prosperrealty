from rest_framework import serializers
from .models import *

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