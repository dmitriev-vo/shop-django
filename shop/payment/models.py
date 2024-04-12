from django.db import models


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(verbose_name="Номер карты", max_length=8)
    name = models.CharField(verbose_name="Имя держателя", max_length=20)
    month = models.CharField(verbose_name="Месяц", max_length=2)
    year = models.CharField(verbose_name="Год", max_length=4)
    code = models.CharField(verbose_name="Код", max_length=3)

    class Meta:
        ordering = ("id",)
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
