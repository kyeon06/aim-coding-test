from django.urls import path

from stocks.views import StockAPIView, StockDetailAPIView

urlpatterns = [
    path("", StockAPIView.as_view(), name="stock-create-list"),
    path("<int:pk>/", StockDetailAPIView.as_view(), name="stock-detail"),
]
