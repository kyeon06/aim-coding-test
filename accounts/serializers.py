from rest_framework import serializers

from accounts.models import Account, Balance


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("__all__",)


class AccountDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Account
        fields = ["user", "balance"]
        read_only_fields = ("balance",)


class BalanceListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Balance
        fields = ["user", "account", "change_balance", "balance_date"]


class BalanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ["user", "account", "change_balance"]

    def create(self, validated_data):
        account = validated_data.get("account")
        change_balance = validated_data.get("change_balance")

        balance = Balance.objects.create(**validated_data)

        instance = Account.objects.get(id=account.id)
        instance.balance += change_balance
        instance.save()

        return balance
