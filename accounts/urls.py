from django.urls import path

from accounts.views import AccountBalanceAPIView, AccountAPIView

urlpatterns = [
    path("", AccountAPIView.as_view(), name="account_create"),
    path("balance/", AccountBalanceAPIView.as_view(), name="account_balance_create"),
]
