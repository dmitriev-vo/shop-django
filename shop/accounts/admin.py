from django.contrib import admin
from .models import Profile, Avatar


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "fullName", "phone", "balance"]


@admin.register(Avatar)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["src", "alt"]
