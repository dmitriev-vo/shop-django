from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CatalogPagination(PageNumberPagination):
    page_size = 5
    page_query_param = "currentPage"
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        last_page_number = self.page.paginator.num_pages
        response_data = {
            "items": data,
            "currentPage": self.page.number,
            "lastPage": last_page_number,
        }

        return Response(response_data)


class SalePagination(PageNumberPagination):
    page_size = 5
    page_query_param = "currentPage"
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        last_page_number = self.page.paginator.num_pages
        response_data = {
            "items": data,
            "currentPage": self.page.number,
            "lastPage": last_page_number,
        }
        return Response(response_data)
