from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from cart.cart import Cart
from .models import Order, CostDelivery
from catalog.models import Product
from accounts.models import Profile
import orders.serializers as sero
from rest_framework import status


class OrdersView(APIView):
    def get(self, request):
        profile = Profile.objects.get(id=request.user.id)
        queryset = Order.objects.filter(created=profile)
        serializer = sero.OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        cart = Cart(request)
        if request.user.is_authenticated:
            order = Order.objects.create(created=request.user)
        else:
            order = Order.objects.create()
        total_cost = 0
        for item in cart:
            total_cost += int(item["total_price"])
            product = Product.objects.get(id=item["product_id"])
            product.count = item["quantity"]
            product.save()
            order.products.add(product)
            order.save()
        order.save()
        request.session.pop("cart")
        data = {
            "orderId": order.id,
        }
        return JsonResponse(data)


class OrderDetailView(APIView):
    def get(self, request, id):
        if request.user.is_authenticated:
            order = Order.objects.get(id=id)
            profile = Profile.objects.get(username=request.user)
            order.created = profile
            order.fullName = profile.fullName
            order.phone = profile.phone
            order.phone = profile.phone
            order.email = profile.email
            order.deliveryType = "ordinary"
            order.city = profile.city
            order.address = profile.address
            serializer = sero.OrderSerializer(order)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id):
        costDelivery = CostDelivery.objects.get(id=1)
        order = Order.objects.get(id=id)
        order.fullName = request.data["fullName"]
        order.phone = request.data["phone"]
        order.email = request.data["email"]
        order.deliveryType = request.data["deliveryType"]
        order.address = request.data["address"]
        order.city = request.data["city"]
        order.paymentType = request.data["paymentType"]
        order.totalCost = request.data["totalCost"]
        if request.data["deliveryType"] == "express":
            order.totalCost = float(order.totalCost) + float(costDelivery.express)
        elif (
            request.data["deliveryType"] == "ordinary" and float(order.totalCost) < 2000
        ):
            order.totalCost = float(order.totalCost) + float(costDelivery.ordinary)
        order.save()
        data = {"orderId": id}
        return JsonResponse(data, safe=False)
