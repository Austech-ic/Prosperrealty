PAYMENT_GATEWAY=[
    ("paystack","Paystack")
]
CHANNELS_CHOICES = [
    ("card_payment", "Card_Payment"),
    ("bank_account", "Cash_Account"),
    ("bank_transfer", "Bank_Transfer")
]

TRANSACTION_STATUS_CHOICES = [
    ("success", "Success"), #success
    ("abandoned", "Abandoned"),
    ("reversed", "Reversed"),
    ("failed", "Failed"), #failed
    ("pending", "pending"),#pending
    ("ongoing", "Ongoing"),
]


STATUS_CHOICES = [
    ("pending", "Pending"),  # active state
    ("Paid", "Paid"),  # closed state
    ("failed", "Failed"),  # active state
  
]