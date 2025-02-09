from datetime import datetime, timezone
from decimal import Decimal

from .helper import to_kobo
from .models import TransactionRecord

def handle_single_invoice_payment(transaction:TransactionRecord, data):
    # ____--------___________-------___________------___________-------
    # If the transaction was for an invoice payment
    # ____--------___________-------___________------___________-------
    try:
        amount_paid=transaction.amount
        transaction.status = data["status"]
        transaction.channel = data["channel"]
        transaction.payed_on = data["paid_at"]

        # transaction.invoice.status=paymentChecker(amount_paid,transaction.invoice)
        transaction.invoice.amountOutstanding -= amount_paid
        transaction.invoice.amountPaid +=amount_paid

        transaction.invoice.payedOn = data["paid_at"]
        transaction.invoice.save()
        transaction.save()
    except Exception as e:
        print("@handle_single_invoice_payment() --> ", e)
        return None




def handle_single_failed_payment(transaction:TransactionRecord, data):

    # ____--------___________-------___________------___________-------
    # If the transaction was for an invoice payment
    # ____--------___________-------___________------___________-------
    try:
        transaction.status = data["status"]
        transaction.channel = data["channel"]
        transaction.payed_on = data["paid_at"]
        transaction.save()
    except Exception as e:
        print("@handle_single_invoice_payment() --> ", e)
        return None