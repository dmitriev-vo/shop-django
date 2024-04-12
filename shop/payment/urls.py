from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("api/payment/<int:id>/", views.PaymentView.as_view(), name="payment"),
]
