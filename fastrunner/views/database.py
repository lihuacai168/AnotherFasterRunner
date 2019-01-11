from rest_framework.viewsets import ModelViewSet
from fastrunner import models, serializers
from FasterRunner import pagination


# Create your views here.


class DataBaseView(ModelViewSet):
    """
    DataBase 增删改查
    """
    queryset = models.DataBase.objects.all().order_by('-update_time')
    pagination_class = pagination.MyCursorPagination
    serializer_class = serializers.DataBaseSerializer
