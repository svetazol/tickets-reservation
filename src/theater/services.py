from theater.models import ReservedTicket


class ReservedTicketService:
    @staticmethod
    def count_performance_reservations(performance, user):
        return ReservedTicket.objects.filter(performance=performance, reserved_by=user).count()
