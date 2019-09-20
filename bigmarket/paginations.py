from rest_framework.pagination import PageNumberPagination


class CommenPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 100
    page_size_query_param = 'page_size'
    page_query_param = 'page'
