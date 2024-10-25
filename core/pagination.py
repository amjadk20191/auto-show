from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response

class DefaultPagination(CursorPagination):
    page_size = 10
    ordering = '-pk'

   