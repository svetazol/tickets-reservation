from rest_framework import viewsets

from theater.models import Category, Performance
from theater.serializers import CategorySerializer, PerformanceSerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    serializer_class = PerformanceSerializer
    queryset = Performance.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
