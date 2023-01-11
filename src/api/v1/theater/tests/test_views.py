from django.test.utils import override_settings
from rest_framework.test import APITestCase

from core.theater.tests import factories


class ReserveTicketTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = factories.UserFactory()
        self.performance = factories.PerformanceFactory()
        self.ticket = factories.TicketFactory()

    def test_create_reserved_ticket__success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/v1/theater/reserved-tickets/",
            data={"performance": self.performance.id, "ticket": self.ticket.id},
            format="json",
        )

        response_data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data["performance"], self.performance.id)
        self.assertEqual(response_data["ticket"], self.ticket.id)
        self.assertEqual(response_data["reserved_by"], self.user.id)

    @override_settings(MAX_TICKET_RESERVATIONS_PER_PERSON=0)
    def test_create_reserved_ticket__failed(self):
        self.reserved_ticket = factories.ReservedTicketFactory(
            ticket=self.ticket, performance=self.performance, reserved_by=self.user
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/v1/theater/reserved-tickets/",
            data={"performance": self.performance.id, "ticket": self.ticket.id},
            format="json",
        )

        response_data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_data, {"non_field_errors": ["The fields performance, ticket must make a unique set."]}
        )
