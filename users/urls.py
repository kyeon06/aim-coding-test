from django.urls import path

from users.views import UserLoginAPIView, UserLogoutAPIView, UserRegisterAPIView

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="user_register"),
    path("login/", UserLoginAPIView.as_view(), name="user_login"),
    path("logout/", UserLogoutAPIView.as_view(), name="user_logout"),
]
