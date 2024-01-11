from rest_framework import serializers

from stocks.models import Stock


class StockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["name", "price"]


class StockCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["code", "name", "price"]


class StockDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


class StockUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["code", "name", "price"]
