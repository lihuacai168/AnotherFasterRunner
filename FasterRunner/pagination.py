from rest_framework import pagination


class MyCursorPagination(pagination.CursorPagination):
    """
    Cursor 光标分页 性能高，安全
    """
    page_size = 9
    ordering = '-update_time'
    page_size_query_param = "pages"
    max_page_size = 20


class MyPageNumberPagination(pagination.PageNumberPagination):
    """
    普通分页，数据量越大性能越差
    """
    page_size = 10
    page_size_query_param = 'size'
    page_query_param = 'page'
    max_page_size = 20


