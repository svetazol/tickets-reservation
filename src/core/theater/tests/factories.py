from datetime import timedelta

import factory
from django.contrib.auth.models import User
from django.utils.timezone import now
from factory.django import DjangoModelFactory

from core.theater.models import Category, Performance, ReservedTicket, Ticket


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("first_name")


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"category name {n}")
    description = factory.Sequence(lambda n: f"category description {n}")


class PerformanceFactory(DjangoModelFactory):
    class Meta:
        model = Performance

    name = factory.Sequence(lambda n: f"performance name {n}")
    description = factory.Sequence(lambda n: f"performance description {n}")
    category = factory.SubFactory(CategoryFactory)
    base_price = factory.Faker("pyint", min_value=0, max_value=1000)
    reservation_start_at = factory.LazyAttribute(lambda o: now() - timedelta(days=2))
    start_at = factory.LazyAttribute(lambda o: now())


class TicketFactory(DjangoModelFactory):
    class Meta:
        model = Ticket

    row_number = factory.Faker("pyint", min_value=0, max_value=1000)
    seat_number = factory.Faker("pyint", min_value=0, max_value=1000)
    price_ratio = factory.Faker("pydecimal", min_value=0, max_value=1000)


class ReservedTicketFactory(DjangoModelFactory):
    class Meta:
        model = ReservedTicket

    performance = factory.SubFactory(PerformanceFactory)
    ticket = factory.SubFactory(TicketFactory)
    reserved_by = factory.SubFactory(UserFactory)
