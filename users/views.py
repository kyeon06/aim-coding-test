from django.utils import timezone
from django.contrib.auth import authenticate, login, logout

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from users.serializers import UserLoginSerializer, UserRegisterSerializer


# api/users/register/
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


# api/users/login/
class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="로그인",
        operation_description="계정명, 비밀번호로 로그인합니다.",
        request_body=UserLoginSerializer,
        responses={
            200: "로그인 성공",
            400: "로그인 실패 또는 정보 미입력",
            401: "USER NOT FOUND",
            403: "USER DEACTIVATED",
        },
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if username is None:
            return Response(
                {"message": "username을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST
            )

        if password is None:
            return Response(
                {"message": "password를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {"message": "해당 유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )

        if not user.is_active:
            return Response(
                {"message": "해당 유저는 비활성화 상태입니다."}, status=status.HTTP_403_FORBIDDEN
            )

        login(request, user)
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        data = {"username": user.username, "message": "로그인 성공"}
        return Response(data=data, status=status.HTTP_200_OK)


# api/users/logout/
class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="로그아웃",
        operation_description="인증된 사용자가 로그아웃합니다.",
        request_body=None,
        responses={200: "로그아웃 성공", 401: "Unauthenticated"},
    )
    def post(self, request):
        user = request.user
        user.last_logout = timezone.now()
        user.save(update_fields=["last_logout"])

        # 로그아웃 수행
        logout(request)

        return Response({"message": "로그아웃 성공"}, status=status.HTTP_200_OK)
