from .models import Bookings
import secrets,string
def generate_comfirmation_no(length=10):
    """Generates invoice id"""
    while True:
        try:
            invoice_id = "".join(
                secrets.choice(
                    string.ascii_uppercase + string.digits + string.ascii_lowercase
                )
                for i in range(length)
            )
            Bookings.objects.get(confirmationNumber__iexact=invoice_id)

        except Bookings.DoesNotExist:
            return invoice_id.upper()