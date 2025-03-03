# Generated by Django 4.2.2 on 2023-06-30 11:08

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("number", models.CharField(max_length=8, verbose_name="Номер карты")),
                ("name", models.CharField(max_length=20, verbose_name="Имя держателя")),
                ("month", models.CharField(max_length=2, verbose_name="Месяц")),
                ("year", models.CharField(max_length=4, verbose_name="Год")),
                ("code", models.CharField(max_length=3, verbose_name="Код")),
            ],
            options={
                "verbose_name": "Платеж",
                "verbose_name_plural": "Платежи",
                "ordering": ("id",),
            },
        ),
    ]
