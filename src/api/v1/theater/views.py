from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from theater.models import Category, Performance, ReservedTicket, Ticket
from theater.permissions import IsOwnerOrReadOnly
from theater.serializers import CategorySerializer, PerformanceSerializer, ReservedTicketSerializer, TicketSerializer


class PerformanceViewSet(ModelViewSet):
    serializer_class = PerformanceSerializer
    queryset = Performance.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        request_body=TicketSerializer(many=True), responses={status.HTTP_201_CREATED: TicketSerializer(many=True)}
    ),
)
class TicketsBulkCreateAPIView(GenericAPIView):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            raise ValidationError({"non_field_error": "data is not type of list"})
        serializer = self.serializer_class(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReservedTicketViewSet(ModelViewSet):
    serializer_class = ReservedTicketSerializer
    queryset = ReservedTicket.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.validate_reserved_tickets_amount(self.request.user)
        serializer.save(reserved_by=self.request.user)
