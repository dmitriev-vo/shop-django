from django.db import models
from catalog.models import Product
from accounts.models import Profile


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    createdAt = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    fullName = models.CharField(verbose_name="Полное имя", max_length=20, default="")
    email = models.EmailField(verbose_name="Электронная почта", default="")
    phone = models.CharField(verbose_name="Телефон", max_length=20, default="")
    deliveryType = models.CharField(
        verbose_name="Тип доставки", default="free", max_length=20
    )
    paymentType = models.CharField(
        verbose_name="Тип платежа", max_length=20, default="online"
    )
    totalCost = models.DecimalField(
        verbose_name="Итоговая стоимость", default=0, max_digits=8, decimal_places=2
    )
    status = models.CharField(verbose_name="Статус", max_length=20, default="accepted")
    city = models.CharField(verbose_name="Город", max_length=20, default="")
    address = models.CharField(verbose_name="Адрес", max_length=20, default="")
    products = models.ManyToManyField(
        Product, related_name="products", verbose_name="Продукты"
    )
    created = models.ForeignKey(
        Profile,
        related_name="profile",
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True,
    )
    paymentError = models.CharField(
        verbose_name="Ошибка оплаты", max_length=20, default=""
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class CostDelivery(models.Model):
    ordinary = models.DecimalField(
        verbose_name="Стоимость обычной доставки",
        default=200,
        max_digits=8,
        decimal_places=2,
    )
    express = models.DecimalField(
        verbose_name="Стоимость экспресс доставки",
        default=500,
        max_digits=8,
        decimal_places=2,
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "Цена за доставку"
        verbose_name_plural = "Цены за доставку"
