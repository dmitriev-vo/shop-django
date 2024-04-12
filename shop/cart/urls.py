from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("api/basket", views.CartDetailView.as_view(), name="cart"),
]
