from django.urls import path as url,re_path
from .views import (

    MakePaymentApiView,

)
from .webhook import PaystackWebhookView
urlpatterns =[
    url("payment/<str:invoiceId>/",MakePaymentApiView.as_view()),
    url("payment/webhook/",PaystackWebhookView.as_view()),
]