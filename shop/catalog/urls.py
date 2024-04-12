from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("api/categories/", views.CategoriesView.as_view(), name="categories"),
    path(
        "api/products/popular/",
        views.PopularProductsView.as_view(),
        name="popular_products",
    ),
    path(
        "api/products/limited/",
        views.LimitedProductsView.as_view(),
        name="limited_products",
    ),
    path("api/banners/", views.BannerProductsView.as_view(), name="banner_products"),
    path(
        "api/product/<int:id>/",
        views.ProductDetailView.as_view(),
        name="product_details",
    ),
    path(
        "api/product/<int:id>/reviews",
        views.ProductReviewsView.as_view(),
        name="product_details",
    ),
    path("api/catalog/", views.CatalogView.as_view(), name="catalog"),
    path("api/sales/", views.SalesView.as_view(), name="sales"),
    path("api/test/", views.BannerProductsView.as_view(), name="test"),
]
