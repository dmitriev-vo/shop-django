from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("api/orders/", views.OrdersView.as_view(), name="orders"),
    path("api/order/<int:id>/", views.OrderDetailView.as_view(), name="order_details"),
]
