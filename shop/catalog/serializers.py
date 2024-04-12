from collections import OrderedDict
from rest_framework import serializers
from catalog import models as m


class ImageSubCategorySerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = m.ImageSubCategory
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class ImageCategorySerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = m.ImageCategory
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class SubCategorySerializer(serializers.ModelSerializer):
    image = ImageSubCategorySerializer(read_only=True)

    class Meta:
        model = m.SubCategory
        fields = ["id", "title", "image"]


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    image = ImageCategorySerializer(read_only=True)

    class Meta:
        model = m.Category
        fields = ["id", "title", "image", "subcategories"]


class ImageProductSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = m.ProductImage
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Tag
        fields = ["id", "name"]


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Specification
        fields = ["name", "value"]


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="user")
    email = serializers.CharField(source="user.email")

    class Meta:
        model = m.ProductReview
        fields = ["author", "email", "text", "rate", "date"]


class ProductSerializer(serializers.ModelSerializer):
    images = ImageProductSerializer(many=True, read_only=True)
    tags = serializers.ListSerializer(child=TagSerializer(), read_only=True)
    specifications = SpecificationSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = m.Product
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        ]


class CatalogSerializer(serializers.ModelSerializer):
    images = ImageProductSerializer(many=True, read_only=True)

    class Meta:
        model = m.Product
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "images",
            "rating",
        ]


class SaleProductSerializer:
    class Meta:
        model = m.Product
        fields = ["id", "price"]


class SaleSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="product.id")
    price = serializers.DecimalField(
        source="product.price", max_digits=8, decimal_places=2
    )
    title = serializers.CharField(source="product.title")
    images = ImageProductSerializer(many=True, read_only=True)

    class Meta:
        model = m.Sale
        fields = ["id", "price", "salePrice", "dateFrom", "dateTo", "title", "images"]
