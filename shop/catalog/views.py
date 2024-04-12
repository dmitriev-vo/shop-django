from django.http import JsonResponse
from rest_framework import generics, views
from rest_framework.response import Response
from .models import Category, Product, Tag, Sale, ProductReview
import catalog.serializers as ser
import catalog.paginations as pag
from accounts.models import Profile
from rest_framework import permissions


class CatalogView(generics.ListAPIView):
    serializer_class = ser.CatalogSerializer
    pagination_class = pag.CatalogPagination

    def get_queryset(self):
        queryset = Product.objects.all()
        if self.request.query_params:
            category = self.request.query_params.get("category")
            if category:
                queryset = queryset.filter(category=category)
            name = self.request.query_params.get("filter[name]")
            if name:
                queryset = queryset.filter(description__icontains=name)
            min_price = self.request.query_params.get("filter[minPrice]")
            if min_price:
                queryset = queryset.filter(price__gte=min_price)
            max_price = self.request.query_params.get("filter[maxPrice]")
            if max_price:
                queryset = queryset.filter(price__lte=max_price)
            freeDelivery = self.request.query_params.get("filter[freeDelivery]")
            if freeDelivery == "true":
                queryset = queryset.filter(freeDelivery=str.title(freeDelivery))
            available = self.request.query_params.get("filter[available]")
            if available == "true":
                queryset = queryset.filter(count__gt=0)
            sort = self.request.query_params.get("sort")
            if sort:
                sortType = self.request.query_params.get("sortType")
                if sortType == "dec":
                    queryset = queryset.order_by(sort)
                if sortType == "inc":
                    queryset = queryset.order_by("-" + sort)
        return queryset


class CategoriesView(views.APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = ser.CategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False)


class PopularProductsView(views.APIView):
    def get(self, request):
        queryset = Product.objects.filter(popular=True)
        serializer = ser.ProductSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class LimitedProductsView(views.APIView):
    def get(self, request):
        queryset = Product.objects.filter(limited=True)
        serializer = ser.ProductSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class BannerProductsView(views.APIView):
    def get(self, request):
        queryset = Product.objects.filter(for_banner=True)
        serializer = ser.ProductSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class ProductDetailView(views.APIView):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        serializer = ser.ProductSerializer(product)
        return JsonResponse(serializer.data, safe=False)


class TagView(views.APIView):
    def get(self, request):
        tag = Tag.objects.get(id=1)
        print("tag", tag)
        serializer = ser.TagSerializer(tag)
        return JsonResponse(serializer.data, safe=False)


class SalesView(generics.ListAPIView):
    serializer_class = ser.SaleSerializer
    pagination_class = pag.SalePagination

    def get_queryset(self):
        queryset = Sale.objects.all()
        return queryset


class ProductReviewsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        product = Product.objects.get(id=id)
        user = Profile.objects.get(username=request.data["author"])
        print("request.data", request.data)
        review = ProductReview.objects.create(
            product=product,
            user=user,
            text=request.data["text"],
            rate=request.data["rate"],
        )
        print("id", id)
        return Response(status=200)
