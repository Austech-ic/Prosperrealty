from django.apps import AppConfig


class AdminDashboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "admin_dashboard"




    def ready(self):
        from .helpers import createCountry,loadProductTag,loadProductStatus,loadProductType

        loadProductTag()
        createCountry()
        loadProductStatus()
        loadProductType()