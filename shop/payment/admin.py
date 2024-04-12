from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "number", "name"]
