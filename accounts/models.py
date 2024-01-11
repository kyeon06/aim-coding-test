from django.db import models

from users.models import User


# 계좌 정보 테이블
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.BigIntegerField(default=0)

    class Meta:
        db_table = "accounts"

    def __str__(self):
        return f"{self.user} : {self.balance}"


# 잔고 입출력 정보 테이블
class Balance(models.Model):
    balance_date = models.DateTimeField(auto_now_add=True)
    change_balance = models.BigIntegerField(default=0)
    account = models.ForeignKey(
        Account, related_name="balance_accounts", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, related_name="balance_users", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "balances"

    def __str__(self):
        return f"{self.user} : {self.change_balance} : {self.balance_date}"
