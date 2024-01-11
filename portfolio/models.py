from django.db import models
from stocks.models import Stock

from users.models import User


TYPE_CHOICES = [("선택", None), ("유형1", "TYPE-1"), ("유형2", "TYPE-2")]


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    risk_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default="선택", blank=True, null=True
    )
    stocks = models.ManyToManyField(Stock, through="PortfolioStock")

    class Meta:
        db_table = "portfolio"


class PortfolioStock(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField("수량", default=0)

    class Meta:
        db_table = "portfolio_stock"


# class Category(models.Model):
#     name = models.CharField(max_length=128)
#     description = models.TextField(max_length=256, null=True, blank=True)

#     class Meta:
#         db_table = "categories"

#     def __str__(self):
#         return self.name
