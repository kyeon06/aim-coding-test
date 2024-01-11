from django.urls import path

from portfolio.views import PortfolioAdviceAPIView

urlpatterns = [
    path("advice/", PortfolioAdviceAPIView.as_view(), name="portfolio_advice")
]
