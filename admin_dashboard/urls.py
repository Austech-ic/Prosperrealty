from django.urls import path
from .views import *


urlpatterns = [
    path("dashboard/product/",ProductApiview.as_view()),
    path("dashboard/product/<uuid:product_id>/",SingleProductApiview.as_view()),
    path("dashboard/product/tags/",ProductTagApiView.as_view()),
    path("dashboard/blog/",BlogAPiView.as_view()),
    path("dashboard/blog/tag/",BlogTagApiView.as_view()),
    path("dashboard/blog/<uuid:blog_id>/",SingleBlogApiView.as_view()),
    path("dashboard/message/",AllMessageApiView.as_view()),
    path("dashboard/message/<uuid:message_id>/",SingleMessageApiView.as_view()),
    path("dashboard/bookings/",BookingsApiview.as_view()),
    path("dashboard/booking/<uuid:booking_id>/",SingleBookingsApiview.as_view()),
    path("dashboard/appointment/",AppointmentAPiView.as_view()),
    path("dashboard/appointment/<uuid:appointment_id>/",SingleAppointmentAPiView.as_view())
    
]