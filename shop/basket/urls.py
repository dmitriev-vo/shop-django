from django.urls import path
from . import views

app_name = "basket"

urlpatterns = [
    path("api/basket/", views.CartDetailView.as_view(), name="basket"),
]