from django.contrib import admin
from catalog import models as m


class ProductInline(admin.StackedInline):
    model = m.ProductImage


@admin.register(m.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "category", "price"]
    inlines = [ProductInline]


@admin.register(m.Sale)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "salePrice"]


@admin.register(m.ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "user", "rate"]


@admin.register(m.Tag)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(m.Specification)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "name", "value"]


@admin.register(m.ImageSubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["src", "alt"]


@admin.register(m.ImageCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["src", "alt"]


@admin.register(m.SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "image"]


@admin.register(m.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "image"]
