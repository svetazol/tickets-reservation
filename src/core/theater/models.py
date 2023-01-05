from django.contrib.auth import get_user_model
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"


class Performance(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="performances")
    start_at = models.DateTimeField()
    reservation_start_at = models.DateTimeField(auto_now_add=True)
    base_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL, related_name="performances")


class Ticket(models.Model):
    row_number = models.IntegerField()
    seat_number = models.IntegerField()
    price_ratio = models.FloatField()


class ReservedTicket(models.Model):
    performance = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="reserved_tickets")
    ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT)
    reserved_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="reserved_tickets")
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["performance", "ticket"]
