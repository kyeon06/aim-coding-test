from rest_framework import serializers

from portfolio.models import TYPE_CHOICES


class PortfolioAdviceSerializer(serializers.Serializer):
    risk_type = serializers.CharField(max_length=20)
