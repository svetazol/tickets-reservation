from django.test import TestCase

from core.theater.services import ReservedTicketService
from core.theater.tests import factories


class ReservedTicketServiceTestCase(TestCase):
    def setUp(self) -> None:
        self.user = factories.UserFactory()
        self.performance = factories.PerformanceFactory()
        self.ticket = factories.TicketFactory()
        self.reserved_ticket = factories.ReservedTicketFactory(
            ticket=self.ticket, performance=self.performance, reserved_by=self.user
        )

    def test_count_performance_reservations__success(self):
        amount = ReservedTicketService.count_performance_reservations(self.performance, self.user)
        self.assertEqual(amount, 1)
