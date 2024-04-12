from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from accounts.models import Profile
import json


class ImageCategory(models.Model):
    src = models.ImageField(
        upload_to="catalog/categories/categories/",
        default="default.jpg",
        verbose_name="Ссылка",
    )
    alt = models.CharField(
        max_length=128, verbose_name="Описание", default="Без описания"
    )

    class Meta:
        verbose_name = "Изображение категорий"
        verbose_name_plural = "Изображения категорий"


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        verbose_name="Название категории", max_length=200, db_index=True
    )
    image = models.ForeignKey(
        ImageCategory,
        on_delete=models.CASCADE,
        related_name="category",
        verbose_name="Изображение",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("title",)
        verbose_name = "Родительская категория"
        verbose_name_plural = "Родительские категории"

    def __str__(self):
        return self.title


class ImageSubCategory(models.Model):
    src = models.ImageField(
        upload_to="catalog/categories/subcategories/",
        default="default.jpg",
        verbose_name="Ссылка",
    )
    alt = models.CharField(
        max_length=128, verbose_name="Описание", default="Без описания"
    )

    class Meta:
        verbose_name = "Изображение дочерних категорий"
        verbose_name_plural = "Изображения дочерних категорий"


class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    id_parrent = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories"
    )
    title = models.CharField(
        verbose_name="Название категории", max_length=200, db_index=True
    )
    image = models.ForeignKey(
        ImageSubCategory,
        on_delete=models.CASCADE,
        related_name="subcategory",
        verbose_name="Изображение",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("title",)
        verbose_name = "Дочерняя категория"
        verbose_name_plural = "Дочернии категории"

    def __str__(self):
        return self.title


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name="Название", max_length=200, null=False, blank=True
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"


def product_images_directory_path(instance, filename: str) -> str:
    path = "catalog/products/product_{pk}/images/{filename}".format(
        pk=instance.product.id, filename=filename
    )
    return path


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        SubCategory, null=True, related_name="categories", on_delete=models.SET_NULL
    )
    price = models.DecimalField(
        verbose_name="Полная стоимость", default=0, max_digits=8, decimal_places=2
    )
    count = models.IntegerField(verbose_name="Количество", default=1)
    date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    title = models.CharField(verbose_name="Название", max_length=100, db_index=True)
    description = models.TextField(verbose_name="Описание", null=False)
    fullDescription = models.TextField(
        verbose_name="Полное описание", null=False, db_index=True
    )
    freeDelivery = models.BooleanField(verbose_name="Бесплатная доставка", default=True)
    rating = models.DecimalField(
        verbose_name="Рейтинг", default=0, max_digits=3, decimal_places=2, max_length=10
    )
    count_buy = models.IntegerField(verbose_name="Количество покупок", default=0)
    popular = models.BooleanField(verbose_name="Популярный", default=False)
    limited = models.BooleanField(verbose_name="Ограниченный", default=False)
    for_banner = models.BooleanField(verbose_name="Для баннера", default=False)
    preview = models.ImageField(
        verbose_name="Изображение", upload_to="catalog/products/"
    )
    tags = models.ManyToManyField(Tag, related_name="tags", verbose_name="Тэги")

    class Meta:
        ordering = ("id",)
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def reviews_count(self):
        reviews = ProductReview.objects.all()
        return len(reviews)

    def average_rating(self):
        reviews = ProductReview.objects.all()
        raiting = 0
        for review in reviews:
            raiting += review.rate
        if len(reviews) != 0:
            avarage_rating = raiting / len(reviews)
        else:
            avarage_rating = 0
        return avarage_rating


class ProductImage(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    src = models.ImageField(
        verbose_name="Ссылка", upload_to=product_images_directory_path
    )
    alt = models.CharField(
        max_length=128, verbose_name="Описание", default="Без описания"
    )


class Specification(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="specifications"
    )
    name = models.CharField(
        verbose_name="Параметр", max_length=200, null=False, blank=True
    )
    value = models.CharField(
        verbose_name="Значение", max_length=200, null=False, blank=True
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "Параметр продукта"
        verbose_name_plural = "Параметры продукта"


class ProductReview(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, related_name="users", null=True
    )
    text = models.TextField(verbose_name="Комментарий", null=False, blank=True)
    rate = models.IntegerField(
        verbose_name="Рейтинг",
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)],
    )
    date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    class Meta:
        ordering = ("date",)
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sales")
    salePrice = models.DecimalField(
        verbose_name="Скидочная стоимость", default=0, max_digits=8, decimal_places=2
    )
    dateFrom = models.DateTimeField()
    dateTo = models.DateTimeField()
