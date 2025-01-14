from django.urls import path
from .views import *


urlpatterns = [
    path("dashboard/product/",ProductApiview.as_view()),
    path("dashboard/product/<uuid:product_id>/",SingleProductApiview.as_view()),
    path("dashboard/product/tags/",ProductTagApiView.as_view()),
    path("dashboard/blog/",BlogAPiView.as_view()),
    path("dashboard/blog/tag/",BlogTagApiView.as_view()),
    path("dashboard/blog/<uuid:blog_id>/",SingleBlogApiView.as_view()),
    
]