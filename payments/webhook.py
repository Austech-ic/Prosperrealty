from prospereality_api.settings import PAYSTACK_SECRET_KEY
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
import hashlib
import hmac
import traceback
from django.views.decorators.csrf import csrf_exempt

from .webhook_handler import handle_single_invoice_payment,handle_single_failed_payment
from .models import TransactionRecord

PAYSTACK_CHARGE_SUCCESS = "charge.success"


class PaystackWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    @csrf_exempt
    def post(self, request):
        try:
            # ____--------___________-------___________------___________-------
            # PAYSTACK AUTHORIZATION
            # ____--------___________-------___________------___________-------
            sig_header = request.headers["x-paystack-signature"]
            secret = PAYSTACK_SECRET_KEY

            hash_ = hmac.new(
                secret.encode("utf-8"), request.body, digestmod=hashlib.sha512
            ).hexdigest()

            # Request not from paystack
            if hash_ != sig_header:
                raise RuntimeError("Unauthorized")

            # ____--------___________-------___________------___________-------
            # MAIN LOGIC
            # ____--------___________-------___________------___________-------
            event: str = request.data["event"]
            data: dict = request.data["data"]
            reference: str = (
                data["reference"]
                if "reference" in data.keys()
                else data["refund_reference"]
            )
            metadata = data.get("metadata", {})

            # ____--------___________-------___________------___________-------
            # LOGIC FOR SINGLE INVOICE TRANSACTION
            # ____--------___________-------___________------___________-------
            if (
                event == PAYSTACK_CHARGE_SUCCESS
                and metadata.get("is_bulk_transaction", "").lower() == "false"
            ):
                # Fetch the transaction
                transaction = TransactionRecord.objects.get(external_reference=reference)
                handle_single_invoice_payment(transaction, data)

            else:
                transaction = TransactionRecord.objects.get(external_reference=reference)
                handle_single_failed_payment(transaction, data)
            return Response({}, status=status.HTTP_200_OK)

        except Exception as e:
            print("@Webhook error ---> ", e)
            traceback.print_exc()
            print(request.data)
            resp = {
                "success": False,
                "message": "Error",
                "errors": str(e),
            }
            return Response(resp, status=status.HTTP_400_BAD_REQUEST)
