from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 30

    def validate_page_number(self, page_number):
        try:
            page_number = int(page_number)
            if page_number < 1:
                return 1
            return page_number
        except (ValueError, TypeError):
            return 1

    def paginate_queryset(self, queryset, request, view=None):
        self.request = request
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        page_number = self.validate_page_number(request.query_params.get(self.page_query_param, 1))
        paginator = Paginator(queryset, page_size)
        try:
            self.page = paginator.page(page_number)
        except (EmptyPage, PageNotAnInteger):
            last_page_number = paginator.num_pages if paginator.num_pages > 0 else 1
            self.page = paginator.page(last_page_number)
        return list(self.page.object_list)

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
            'total_pages': self.page.paginator.num_pages,
        })


class MedicalCardEntryPagination(CustomPageNumberPagination):
    page_size = 10
    max_page_size = 20

    def paginate_queryset(self, queryset, request, view=None):
        queryset = queryset.order_by('-visit_date')
        return super().paginate_queryset(queryset, request, view)