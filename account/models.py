import re
import secrets
from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid
from admin_dashboard.contants import SPECIAL_CHARS_REGEX
from .constant import GENDER

class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role=models.CharField(max_length=100,null=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email or phone_number is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self,email, password, **extra_fields):
        """
        Create and save a User with the given email, phone_number and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))

        # if not phone_number:
        #     raise ValueError(_("The phone number must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email phone_number and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    def upload_to(instance, filename):
        url = re.sub(
            SPECIAL_CHARS_REGEX,
            "_",
            "images/profile/{filename}".format(filename=instance.first_name),
        )
        return url
    username=models.CharField(max_length=500,null=True)
    first_name=None
    last_name=None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True, blank=True, null=True)
    phoneNumber=models.CharField(max_length=500,null=True)
    gender=models.CharField(choices=GENDER,null=True,max_length=10)
    nationality=models.CharField(max_length=100,null=True)
    address=models.CharField(max_length=500,null=True)
    confirm_password = models.CharField(_('password'), max_length=128)
    role=models.ManyToManyField(Role)
    image=models.ImageField(upload_to=upload_to,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [""]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

    def is_host(cls):
        if "HOST" in cls.role.values_list("role",flat=True):
            return True
        return False
    

    
