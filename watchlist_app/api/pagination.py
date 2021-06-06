from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination, CursorPagination


class WatchListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'size'
    max_page_size = 20


class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 20


class WatchListCPagination(CursorPagination):
    page_size = 5
