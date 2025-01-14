from django.db import models
from admin_dashboard.models import Product
import uuid
from properties.constant import (
    BOOKING_STATUS
)

class BaseModel(models.Model):
    id=models.UUIDField(primary_key=True,db_index=True,default=uuid.uuid4)

    class Meta:
        abstract=True


class TransactionRecord(BaseModel):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    email=models.EmailField(null=False)
    amount=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    amountpaid=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    paymentStatus=models.CharField(max_length=20,default="pending",choices=BOOKING_STATUS)
    amountOutstanding=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    paidOn=models.DateField(null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)