import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework import status
from orders.models import Order


class PaymentView(APIView):
    def post(self, request, id):
        print('создается оплата')
        order = Order.objects.get(id=id)
        if (
            len(request.data["number"]) > 8
            or int(request.data["number"]) % 2 != 0
            or 13 < int(request.data["month"]) < 1
            or int(request.data["year"]) < datetime.date.today().year
            or 999 < int(request.data["code"]) < 1
        ):
            order.status = "Ошибка оплаты"
            order.paymentError = "Ошибка"
            order.save()
            return Response(status=status.HTTP_400_BAD_REQUEST)
        print('создается оплата')
        payment = Payment.objects.create(
            number=request.data["number"],
            name=request.data["name"],
            month=request.data["month"],
            year=request.data["year"],
            code=request.data["code"],
        )
        order.status = "Оплачен"
        order.save()
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)
