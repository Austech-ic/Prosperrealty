from .models import *
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField,Base64FileField
from account.serializers import UserSerializer

class Base64ImagesField(Base64ImageField):
    class Meta:
        swagger_schema_fields = {
            'type': 'String',
            'title': 'Image Content',
            'description': 'Content of the base64 encoded images',
            'read_only': False  # <-- FIX
        }

class ImagesSerializer(serializers.Serializer):
    id=serializers.UUIDField(required=False,allow_null=True)
    image=Base64ImagesField(required=True)

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
                    image=image
                )
        return product
    

    def update(self, instance, validated_data):
        images=validated_data.pop("images",None)

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
            "images"
        ]

    
    def get_productStatus(self,obj):
        return obj.productStatus.name

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
                    image=image
                )
        return blog
    


    def update(self, instance, validated_data):
        images=validated_data.pop("images",None)
        image_Ids=[]
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

class SingleBlogReadSerializer(serializers.ModelSerializer):
    images=ImagesSerializer(many=True,required=False)
    tag=BlogTagSerializer(many=True)
    created_by=UserSerializer()
    viewsCount=serializers.SerializerMethodField()
    otherBlog=serializers.SerializerMethodField()
    class Meta:
        model=Blog
        fields="__all__"



    def get_otherBlog(self,obj):
        otherBlogs=self.Meta.model.objects.exclude(id=obj.id).order_by("-createdAt")[:3]
        return BlogReadSerializer(otherBlogs,many=True).data


    def get_viewsCount(self,obj):
        return obj.views.first().count if obj.views.first() else 0
    
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
    class Meta:
        model=ProductType
        fields="__all__"