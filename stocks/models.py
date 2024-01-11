from django.db import models


class Stock(models.Model):
    code = models.CharField("증권코드", max_length=128, unique=True)
    name = models.CharField("증권이름", max_length=128)
    price = models.IntegerField("증권가격")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "stocks"

    def __str__(self):
        return self.code
