from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from theater.models import Category, Performance, Ticket
from theater.serializers import CategorySerializer, PerformanceSerializer, TicketSerializer


class PerformanceViewSet(ModelViewSet):
    serializer_class = PerformanceSerializer
    queryset = Performance.objects.all()


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        request_body=TicketSerializer(many=True), responses={status.HTTP_201_CREATED: TicketSerializer(many=True)}
    ),
)
class TicketsBulkCreateAPIView(GenericAPIView):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def post(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            raise ValidationError({"non_field_error": "data is not type of list"})
        serializer = self.serializer_class(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
