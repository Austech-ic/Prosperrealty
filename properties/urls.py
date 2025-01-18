from django.urls import path
from .views import *

urlpatterns = [
   path("product/booking/",ProductBookingApiView.as_view()),
   path("product/",ProductApiview.as_view(),name="home_product"),
   path("blog/",BlogAPiView.as_view()),
   path("product/<uuid:product_id>/",SingleProductApiView.as_view()),
   path("blog/<uuid:blog_id>/",SingleBlogApiview.as_view(),name="SingleBlogApiview"),
   path("message/",MessageWriteApiView.as_view()),
   path("blog/<uuid:blog_id>/comment/",CommentApiView.as_view()),
   path("state/",StateApiView.as_view()),
   path("country/",CountrypiView.as_view()),
   path("state/local-govt/<str:state_name>/",LocalGovernmentApiView.as_view()),
   path("product/type/",ProductTypeApiView.as_view()),
   path("product/status/",ProductStatusApiView.as_view()),
   path("appointments/",AppointmentApiView.as_view()),
   path("product/<uuid:property_id>/booked/date/",ProductBookedDateApiview.as_view())
]
