from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.theater.views import (
    CategoryViewSet,
    PerformanceViewSet,
    ReservedTicketViewSet,
    TicketsBulkCreateAPIView,
    TicketViewSet,
)

router = DefaultRouter()
router.register("performances", PerformanceViewSet, basename="performance")
router.register("categories", CategoryViewSet, basename="category")
router.register("tickets", TicketViewSet, basename="ticket")
router.register("reserved-tickets", ReservedTicketViewSet, basename="reserved-tickets")

app_name = "theater"
urlpatterns = [path("tickets/bulk", TicketsBulkCreateAPIView.as_view(), name="ticket-bulk-create"), *router.urls]
