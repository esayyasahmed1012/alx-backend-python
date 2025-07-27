# chats/pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # Total number of items
            'next': self.get_next_link(),        # URL to next page
            'previous': self.get_previous_link(), # URL to previous page
            'results': data                      # Paginated data
        })