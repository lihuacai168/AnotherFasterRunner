from django_filters import rest_framework as django_filters
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from system.serializers.log_record_serializer import LogRecordSerializer

from .models import LogRecord


class LogRecordFilter(django_filters.FilterSet):
    request_id = django_filters.CharFilter(field_name="request_id", lookup_expr="exact")
    message = django_filters.CharFilter(field_name="message", lookup_expr="icontains")

    class Meta:
        model = LogRecord
        fields = ["request_id", "message"]


class LogRecordViewSet(viewsets.ModelViewSet):
    queryset = LogRecord.objects.all()
    serializer_class = LogRecordSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = LogRecordFilter
    ordering_fields = ["create_time"]
    ordering = ["create_time"]

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
