from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="AIM CODING TEST",
        default_version="v1",
        description="자문서버 구축 프로젝트",
        contact=openapi.Contact(email="jkyeon06@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # admin
    path("admin/", admin.site.urls),

    # api
    path("api/users/", include("users.urls")),
    path("api/accounts/", include("accounts.urls")),
    path("api/stocks/", include("stocks.urls")),

    # swagger
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]