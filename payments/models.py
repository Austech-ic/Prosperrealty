from decimal import Decimal
from django.db import models
from admin_dashboard.models import Product
from properties.models import Bookings
import uuid
from properties.constant import (
    BOOKING_STATUS
)
from django.conf import settings
from .constant import (

    CHANNELS_CHOICES,
    PAYMENT_GATEWAY,

)
from django.core.validators import RegexValidator,MinValueValidator

class BaseModel(models.Model):
    id=models.UUIDField(primary_key=True,db_index=True,default=uuid.uuid4)

    class Meta:
        abstract=True


class TransactionInvoice(BaseModel):
    invoiceId=models.CharField(max_length=10,null=True,blank=True)
    booking=models.ForeignKey(Bookings,on_delete=models.CASCADE,null=True,blank=True)
    payedOn = models.DateTimeField(blank=True, null=True)
    amountPaid = models.DecimalField(
        max_digits=20, decimal_places=2, null=False, blank=False, default=0.00
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="invoice"
    )
    amountOutstanding = models.DecimalField(
        max_digits=20, decimal_places=2, null=False, blank=False,default=0.00
    )
    totalAmount = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True,default=0.00
    )
    status = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        choices=BOOKING_STATUS,
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TransactionRecord(BaseModel):
    booking=models.ForeignKey(Bookings,on_delete=models.SET_NULL,null=True,blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="Transactions"
    )
    email = models.EmailField(blank=True, null=True)
    reference = models.UUIDField(
        unique=True, null=False, blank=False, editable=False, default=uuid.uuid4
    )
    invoice = models.ForeignKey(
        TransactionInvoice, on_delete=models.CASCADE, blank=True, null=True,related_name="invoiceTransactions"
    )
    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=False,
        blank=False,
        validators=[MinValueValidator(Decimal("1.00"))],
    )
    external_reference = models.TextField(blank=True, default="")
    authorization_url = models.TextField(blank=True, default="")
    access_code=models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        choices=BOOKING_STATUS,
        default=dict(BOOKING_STATUS)["pending"].lower(),
    )
    gateway=models.CharField(max_length=30,choices=PAYMENT_GATEWAY)
    channel = models.CharField(
        max_length=20, blank=False, null=False, choices=CHANNELS_CHOICES, default="card_payment"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    payed_on = models.DateTimeField(null=True, blank=True)