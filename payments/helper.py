import secrets,string
from .models import TransactionInvoice

def to_kobo(amount):
    """Converts an amount to kobo"""
    return amount * 100

def generate_invoice_id(length=6):
    """Generates invoice id"""
    while True:
        try:
            invoice_id = "".join(
                secrets.choice(
                    string.ascii_uppercase + string.digits + string.ascii_lowercase
                )
                for i in range(length)
            )
            TransactionInvoice.objects.get(invoiceId=invoice_id)

        except TransactionInvoice.DoesNotExist:
            return invoice_id