from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.theater.models import Category, Performance, ReservedTicket, Ticket
from core.theater.services import ReservedTicketService


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PerformanceSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Performance
        fields = "__all__"


class TicketListSerializer(serializers.ListSerializer):
    def validate(self, data):
        # row_number has to start from 1 with step 1
        row_numbers = sorted(i["row_numbers"] for i in data)
        if row_numbers[0] != 1:
            raise ValidationError("row_number has to include 1")
        for i, j in zip(row_numbers[:-1], row_numbers[1:]):
            if j - i > 1:
                raise ValidationError(f"No row_number between {i} and {j}")
        return data


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
        list_serializer_class = TicketListSerializer


class ReservedTicketSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ReservedTicket
        fields = "__all__"

    def validate_reserved_tickets_amount(self, user):
        amount = ReservedTicketService.count_performance_reservations(self.performance, user)
        if amount > settings.MAX_TICKET_RESERVATIONS_PER_PERSON:
            raise ValidationError("Exceed max tickets reserv")