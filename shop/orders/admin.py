from django.contrib import admin
from .models import Order, CostDelivery


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "createdAt", "fullName", "created"]


@admin.register(CostDelivery)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "ordinary", "express"]
