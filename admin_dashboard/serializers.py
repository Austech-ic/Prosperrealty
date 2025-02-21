from .models import *
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField,Base64FileField,HybridImageField
from account.serializers import UserSerializer
from .helpers import format_number
# 
from properties.models import Comment

class Base64ImagesField(HybridImageField):
    class Meta:
        swagger_schema_fields = {
            'type': 'String',
            'title': 'Image Content',
            'description': 'Content of the base64 encoded images',
            'read_only': False  # <-- FIX
        }

class ImagesSerializer(serializers.Serializer):
    id=serializers.UUIDField(required=False,allow_null=True)
    image=Base64ImagesField(required=False)

class ProductTagSerializer(serializers.ModelSerializer):
    class Mata:
        model=ProductTag
        fields=[
            "name",
            "id"
        ]

class ProductWriteSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(required=False,allow_null=True)
    images=ImagesSerializer(many=True,required=False)
    class Meta:
        model=Product
        exclude=[
            "slug",
            "created_by"
        ]

    def validate_tag(self, value):
        tag=None
        if not all(isinstance(tag.id, uuid.UUID) for tag in value):
            raise serializers.ValidationError("Invalid UUID for tag.")
        tag=[tag.id for tag in value]
        return tag

    def create(self, validated_data):
        images=validated_data.pop("images",None)
        product=super().create(validated_data)
        if images:
            for image in images:
                ProductImage.objects.create(
                    product=product,
                    **image
                )
        return product
    

    def update(self, instance, validated_data):
        images=validated_data.pop("images",None)
        tags = validated_data.pop("tag", None)  # Pop 'tag' field from validated_data
        if tags is not None:
            instance.tag.set(tags) 
        image_Ids=[]
        if images: # Clear existing images
            for image_data in images:
                image_id = image_data.get('id',None)
                if image_id and image_id != None: 
                    image_instance =ProductImage.objects.get(id=image_id)
                    image_instance.image = image_data.get('image', image_instance.image)
                    image_instance.save()
                    image_Ids.append(image_instance.id)
                else:
                    requestImage=ProductImage.objects.create(product=instance,**image_data)
                    image_Ids.append(requestImage.id)

        ProductImage.objects.filter(product=instance).exclude(id__in=image_Ids).delete()
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
  
class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductTag
        fields="__all__"

class ProductReadSerializer(serializers.ModelSerializer):
    images=ImagesSerializer(many=True)
    productStatus=serializers.SerializerMethodField()
    class Meta:
        model=Product
        fields=[
            "id",
            "price",
            "location",
            "name",
            "productStatus",
            "frequency",
            "sqft",
            "bathroom",
            "buildYear",
            "bedroom",
            "images",
            "currency",
            "productCategory"
        ]

    
    def get_productStatus(self,obj):
        return obj.productStatus.name if obj.productStatus else None
    
class ProductSingleReadSerializer(serializers.ModelSerializer):
    images=ImagesSerializer(many=True)
    tag=ProductTagSerializer(many=True)
    created_by=UserSerializer()
    class Meta:
        model=Product
        fields="__all__"
        depth=1

class WriteBlogSerializer(serializers.ModelSerializer):
    images=ImagesSerializer(many=True,required=False)
    class Meta:
        model=Blog
        exclude=[
            "created_by",
            "slug"
        ]

    def validate_tag(self, value):
        tag=None
        if not all(isinstance(tag.id, uuid.UUID) for tag in value):
            raise serializers.ValidationError("Invalid UUID for tag.")
        tag=[tag.id for tag in value]
        return tag

    def create(self, validated_data):
        images=validated_data.pop("images",None)
        blog= super().create(validated_data)
        
        if images:
            for image in images:
                BlogImage.objects.create(
                    blog=blog,
                    **image
                    # image=image["image"]
                )
        
        return blog
    


    def update(self, instance, validated_data):
        images=validated_data.pop("images",None)
        image_Ids=[]
        tags = validated_data.pop("tag", None)  # Pop 'tag' field from validated_data
        if tags is not None:
            instance.tag.set(tags) 
        if images: # Clear existing images
            for image_data in images:
                image_id = image_data.get('id',None)
                if image_id and image_id != None: 
                    image_instance =BlogImage.objects.get(id=image_id)
                    image_instance.image = image_data.get('image', image_instance.image)
                    image_instance.save()
                    image_Ids.append(image_instance.id)
                else:
                    requestImage=BlogImage.objects.create(blog=instance,**image_data)
                    image_Ids.append(requestImage.id)

        BlogImage.objects.filter(blog=instance).exclude(id__in=image_Ids).delete()
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model=BlogTag
        fields="__all__"

class BlogReadSerializer(serializers.ModelSerializer):
    images=ImagesSerializer(many=True,required=False)
    tag=BlogTagSerializer(many=True)
    created_by=UserSerializer()
    class Meta:
        model=Blog
        exclude=[
            "description"
        ]

class CommentSerializer(serializers.ModelSerializer):
    createdBy=UserSerializer(read_only=True)
    can_delete=serializers.SerializerMethodField()
    class Meta:
        model=Comment
        exclude=[
            "blog",
        ]


    def get_can_delete(self,obj):
        req=self.context.get("request",None)
        if req:
            if obj.createdBy == req.user:
                return True
            return False

class SingleBlogReadSerializer(serializers.ModelSerializer):
    images=ImagesSerializer(many=True,required=False)
    tag=BlogTagSerializer(many=True)
    created_by=UserSerializer()
    viewsCount=serializers.SerializerMethodField()
    otherBlog=serializers.SerializerMethodField()
    comments=serializers.SerializerMethodField()
    has_more=serializers.SerializerMethodField()
    class Meta:
        model=Blog
        fields="__all__"


    def get_otherBlog(self,obj):
        otherBlogs=self.Meta.model.objects.exclude(id=obj.id).order_by("-createdAt")[:3]
        return BlogReadSerializer(otherBlogs,many=True).data


    def get_viewsCount(self,obj):
        return format_number(obj.views.first().count) if obj.views.first() else 0
    
    def get_comments(self,obj):
        comments=obj.comments.order_by("-createdAt")[:3]
        return CommentSerializer(comments,many=True).data

    def get_has_more(self,obj):
        if obj.comments.count() > 3:
            return True
        else :
            return False
    
class DashbordBlogReadSerializer(serializers.ModelSerializer):
    viewsCount=serializers.SerializerMethodField()
    commentCount=serializers.SerializerMethodField()
    class Meta:
        model=Blog
        fields=[
            "title",
            "createdAt",
            "updatedAt",
            "viewsCount",
            "commentCount"
        ]


    def get_viewsCount(self,obj):
        return obj.views.first().count if obj.views.first() else 0
    
    def get_commentCount(self,obj):
        return obj.comments.count()
    
class StateGetSerializer(serializers.ModelSerializer):
    class Meta:
        model=State
        fields="__all__"

class CountryGetSerializer(serializers.ModelSerializer):
    class Meta:
        model=Country
        fields="__all__"

class LocalGovernmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=LocalGovt
        fields=[
            "LGA",
            "id"
        ]

class ProductStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductStatus
        fields="__all__"

class ProductTypeSerializer(serializers.ModelSerializer):
    productCount=serializers.SerializerMethodField()
    class Meta:
        model=ProductType
        fields="__all__"


    def get_productCount(self,obj):
        return obj.productTypes.count()