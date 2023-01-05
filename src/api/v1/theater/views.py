from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.theater.models import Category, Performance, ReservedTicket, Ticket
from core.theater.permissions import IsOwnerOrReadOnly
from core.theater.serializers import (
    CategorySerializer,
    PerformanceSerializer,
    ReservedTicketSerializer,
    TicketSerializer,
)
from core.theater.services import ReservedTicketService


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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.validate_logic(serializer)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def validate_logic(self, serializer):
        performance = serializer.validated_data["performance"]
        self._validate_open_reservation(performance)
        self._validate_reserved_tickets_amount(performance, self.request.user)

    def _validate_reserved_tickets_amount(self, performance, user):
        amount = ReservedTicketService.count_performance_reservations(performance, user)
        if amount > settings.MAX_TICKET_RESERVATIONS_PER_PERSON:
            raise ValidationError("Exceed max tickets reservations")

    def _validate_open_reservation(self, performance):
        if now() < performance.reservation_start_at:
            raise ValidationError("Reservation for the performance is not open yet")

    def perform_create(self, serializer):
        serializer.save(reserved_by=self.request.user)
