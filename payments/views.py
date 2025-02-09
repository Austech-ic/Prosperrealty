from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .models import TransactionRecord,TransactionInvoice
from django.db import transaction
from decimal import Decimal
from django.conf import settings
from .services import PaystackPaymentService
from .helper import to_kobo
from .serializers import TransactionHistorySerializer,TransactionHistorySerializerDeatils
from utils.app_response import app_response
from utils.error_handler import error_handler
# Create your views here.

paystackService=PaystackPaymentService()

class MakePaymentApiView(APIView):

    def post(self,request,invoiceId):
        try:
            with transaction.atomic():
                #Get the invoice from service Invoice
                invoice=TransactionInvoice.objects.select_related(
                    "product"
                ).get(invoiceId=invoiceId)

                if invoice.amountOutstanding == Decimal(0.00):
                    raise RuntimeError("Invoices already paid for")
                
                if invoice.status.lower() =="paid":
                    raise RuntimeError("Invoices already paid for")

                paystack_transaction = paystackService.initialize_transaction(
                    amount=to_kobo(invoice.amountOutstanding),
                    email=request.user.email,
                    # channels=["bank_transfer"],
                    metadata={
                        "is_bulk_transaction": False,
                    },
                )
                if not paystack_transaction:
                    raise RuntimeError("Unable to complete transaction")
                
                trans=TransactionRecord.objects.create(
                    user=request.user,
                    email=request.user.email,
                    invoice=invoice,
                    external_reference=paystack_transaction["reference"],
                    authorization_url=paystack_transaction["authorization_url"]
                    if "authorization_url" in list(paystack_transaction.keys())
                    else "",
                    access_code=paystack_transaction["access_code"]
                    if "access_code" in list(paystack_transaction.keys())
                    else "",
                    amount=invoice.amountOutstanding ,
                    gateway="paystack",
                    channel="bank_transfer"
                )

                return app_response(
                    success=True,
                    data=TransactionHistorySerializer(trans).data,
                    message="PAYMENT ACCOUNT GENERATED SUCCESSFULLY",
                    http_status=status.HTTP_200_OK
                ) 
        except TransactionInvoice.DoesNotExist as e:
            return app_response(
                success=False,
                data=None,
                message="invalid Invoice Id",
                http_status=status.HTTP_400_BAD_REQUEST
            )  
        except Exception as e:
            return app_response(
                success=False,
                data=None,
                message=error_handler(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )  