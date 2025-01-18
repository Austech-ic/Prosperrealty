from properties.models import BlogViews
from admin_dashboard.models import Blog,Visitors
from django.utils.deprecation import MiddlewareMixin
# from datetime import datetime,timezone
from django.urls import resolve
import calendar
from django.utils.timezone import now
from django.db import transaction


class BlogViewPageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Resolve the URL path to get the view name and arguments
        resolver_match = resolve(request.path)
        # Check if the resolved view corresponds to the Blog view
        if resolver_match.view_name == 'SingleBlogApiview':
            # Extract the blog_id from the URL kwargs
            blog_id = resolver_match.kwargs.get('blog_id')
            
            # Ensure the blog_id is valid and perform the logic
            if blog_id:
                try:
                    blog = Blog.objects.get(id=blog_id)
                    obj, created = BlogViews.objects.get_or_create(
                        blog=blog,
                        defaults={
                            "blog": blog,
                            "count": 1
                        }
                    )
                    if not created:
                        obj.count += 1
                        obj.save()
                except Blog.DoesNotExist:
                    pass  # Handle the case where the blog does not exist, if needed
        
        # Continue processing the request
        return None


class VisitorsMiddleware(MiddlewareMixin):
        
    def process_request(self, request):

        resolver_match = resolve(request.path)
        #home,property,blog
        if resolver_match.view_name == "home_product":
            date_obj = now()
            month=date_obj.month
            year=date_obj.year
            with transaction.atomic():
                obj, created = Visitors.objects.get_or_create(
                    month=calendar.month_abbr[month],
                    year=str(year),
                    defaults={
                        "month": calendar.month_abbr[month],
                        "year": str(year),
                        "count": 1,  # Initialize count for new records
                    },
                )
                if not created:
                    obj.count += 1
                    obj.save()


        return None