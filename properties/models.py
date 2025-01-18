import uuid
from django.db import models
from admin_dashboard.models import Product
from admin_dashboard.models import Blog
from .constant import (
    BOOKING_STATUS,
    CONTACT_METHOD
)
from django.conf import settings
# Create your models here.

class BaseModel(models.Model):
    id=models.UUIDField(primary_key=True,db_index=True,default=uuid.uuid4)

    class Meta:
        abstract=True

class Bookings(BaseModel):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    email=models.EmailField(null=True)
    initiated_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="bookings",null=True)
    phoneNumber=models.CharField(max_length=20,null=True,blank=True)
    fullName=models.CharField(max_length=225,null=True)
    bookingStatus=models.CharField(max_length=30,default="pending",choices=BOOKING_STATUS)
    specialRequest=models.TextField(null=True)
    adultsCount=models.BigIntegerField(default=0)
    childrenCount=models.BigIntegerField(default=0)
    infantsCount=models.BigIntegerField(default=0)
    petCount=models.BigIntegerField(default=0)
    checkInDate=models.DateField(null=True)
    checkOutDate=models.DateField(null=True)
    stayDuration=models.BigIntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.checkInDate and self.checkOutDate:
            self.stayDuration = (self.checkOutDate - self.checkInDate).days
        else:
            self.stayDuration = 0
        super().save(*args, **kwargs)

class Messages(BaseModel):
    firstName=models.CharField(max_length=225,null=True)
    lastName=models.CharField(max_length=225,null=True)
    email=models.EmailField(null=True)
    phoneNumber=models.CharField(max_length=225,null=True)
    message=models.TextField(null=True)
    inquiryType=models.CharField(max_length=225,null=True)
    aboutUs=models.CharField(max_length=500,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class Comment(BaseModel):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,null=False,blank=False,related_name="comments")
    text=models.CharField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class BlogViews(BaseModel):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,null=False,blank=False,related_name="views")
    count=models.BigIntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class Appointment(BaseModel):
    agentDetail=models.ForeignKey(
        settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name="agents"
    )
    userDetail=models.ForeignKey(
        settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name="users"
    )
    property=models.ForeignKey(
        Product,on_delete=models.CASCADE,null=True
    )
    preferredDate=models.DateField(null=True)
    preferredTime=models.TimeField(null=True)
    contactMethod=models.CharField(choices=CONTACT_METHOD,max_length=100,default="in_person")
    purpose=models.CharField(max_length=500,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)