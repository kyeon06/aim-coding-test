from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from users.serializers import UserLoginSerializer, UserRegisterSerializer


class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="회원가입",
        operation_description="계정명, 비밀번호를 입력받아 회원가입을 진행합니다.",
        request_body=UserRegisterSerializer,
        responses={201: "회원가입 완료", 400: "회원가입 실패"},
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            data = {"username": user.username, "message": "회원가입 완료"}

            return Response(data=data, status=status.HTTP_201_CREATED)

        data = {"message": "회원가입 실패", "error": serializer.error_messages}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="로그인",
        operation_description="계정명, 비밀번호로 로그인합니다.",
        request_body=UserLoginSerializer,
        responses={200: "로그인 성공", 400: "로그인 실패"},
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogoutAPIView(APIView):
    pass
