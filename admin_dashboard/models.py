from django.db import models
import uuid
from .contants import (
    CURRENCY,FREQUENCY,PRODUCT_CATEGORY,PRODUCT_TYPE,
    SPECIAL_CHARS_REGEX,CATEGORY,PACKING,PROPERTY_STATUS,
)
import re
from django.conf import settings


class BaseModel(models.Model):
    id=models.UUIDField(primary_key=True,db_index=True,default=uuid.uuid4)

    class Meta:
        abstract=True

class Country(BaseModel):
    name=models.CharField(max_length=225)
    created_at=models.DateTimeField(auto_now_add=True)

class State(BaseModel):
    country=models.ForeignKey(Country,on_delete=models.CASCADE,null=True,related_name="countries")
    name=models.CharField(max_length=225)
    created_at=models.DateTimeField(auto_now_add=True,null=True)

class LocalGovt(BaseModel):
    state=models.ForeignKey(State,on_delete=models.CASCADE,related_name="states",db_index=True)
    LGA=models.CharField(max_length=225)
    created_at=models.DateTimeField(auto_now_add=True,null=True)

class ProductType(BaseModel):
    name=models.CharField(max_length=225)
    created_at=models.DateTimeField(auto_now_add=True)

class ProductStatus(BaseModel):
    name=models.CharField(max_length=225)
    created_at=models.DateTimeField(auto_now_add=True)

class ProductTag(BaseModel):
    name=models.CharField(max_length=500,null=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class Product(BaseModel):
    name=models.CharField(max_length=500,null=False,blank=False)
    country=models.ForeignKey(Country,on_delete=models.SET_NULL,related_name="productCountry",null=True)
    state=models.ForeignKey(State,on_delete=models.SET_NULL,related_name="productState",null=True)
    city=models.ForeignKey(LocalGovt,on_delete=models.SET_NULL,related_name="productCity",null=True)
    location=models.CharField(max_length=500,null=False,blank=False)
    tourUrl=models.URLField(null=True,blank=True)
    description=models.TextField()
    slug=models.SlugField(null=True)
    currency=models.CharField(choices=CURRENCY,max_length=100,default="NG")
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="products",null=True,blank=True)
    price=models.DecimalField(decimal_places=2,max_digits=10,default=0.00)
    productStatus=models.ForeignKey(ProductStatus,on_delete=models.SET_NULL,related_name="products",null=True)
    productCategory=models.CharField(choices=PRODUCT_CATEGORY,max_length=500,null=True,blank=True)
    frequency=models.CharField(null=True,choices=FREQUENCY,max_length=20,blank=True)
    productType=models.ForeignKey(ProductType,on_delete=models.SET_NULL,related_name="productTypes",null=True)
    sqft=models.CharField(max_length=500,null=True,blank=True)
    bathroom=models.IntegerField(default=0)
    bedroom=models.IntegerField(default=0)
    buildYear=models.DateField(null=True,blank=True)
    packing=models.CharField(choices=PACKING,max_length=10,default="yes")
    tag=models.ManyToManyField(ProductTag,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class ProductImage(BaseModel):
    def upload_to(instance, filename):
        url = re.sub(
            SPECIAL_CHARS_REGEX,
            "_",
            "prospereality/images/{filename}".format(filename=instance),
        )
        return url
    image=models.ImageField(upload_to=upload_to,max_length=500)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images",db_index=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class BlogTag(BaseModel):
    name=models.CharField(max_length=500,null=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class Blog(BaseModel):
    title=models.CharField(max_length=500,null=False,blank=False)
    description=models.TextField()
    slug=models.SlugField(null=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="blogs")
    tag=models.ManyToManyField(BlogTag,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class BlogImage(BaseModel):
    def upload_to(instance, filename):
        url = re.sub(
            SPECIAL_CHARS_REGEX,
            "_",
            "prospereality/images/{filename}".format(filename=instance),
        )
        return url
    image=models.ImageField(upload_to=upload_to,max_length=500)
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name="images",db_index=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

# class MostViewPage(models.Model):
#     count=models.BigIntegerField(default=1)
#     month=models.CharField(max_length=20,null=True)
#     year=models.CharField(null=True,max_length=7)
#     created_at=models.DateTimeField(auto_now_add=True,null=True)