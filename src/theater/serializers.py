from rest_framework import serializers

from theater.models import Performance, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = []


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        exclude = []
