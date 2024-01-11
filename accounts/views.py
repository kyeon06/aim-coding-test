from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from accounts.models import Account, Balance
from accounts.serializers import (
    AccountDetailSerializer,
    AccountSerializer,
    BalanceCreateSerializer,
    BalanceListSerializer,
)


# api/accounts/
class AccountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="계좌 잔고 조회",
        operation_description="보유하고 있는 계좌의 잔고를 확인할 수 있다.",
        request_body=None,
        responses={
            200: AccountDetailSerializer,
            401: "Unauthenticated",
            404: "Not Found",
        },
    )
    def get(self, request):
        user = request.user

        try:
            user_account = Account.objects.get(user=user)
        except:
            return Response(
                {"message": "계좌 정보가 존재하지 않습니다. 생성해주세요."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AccountDetailSerializer(user_account)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id="계좌 생성",
        operation_description="입출금 용도의 계좌를 생성할 수 있다.",
        request_body=None,
        responses={
            201: AccountDetailSerializer,
            401: "Unauthenticated",
            400: "계좌가 이미 존재할 경우 OR 잘못된 요청",
        },
    )
    def post(self, request):
        user = request.user

        is_exists = Account.objects.filter(user=user).exists()
        if is_exists:
            return Response(
                {"message": "계좌가 이미 존재합니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        data = {"user": user.id}

        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            saved_data = serializer.save()
            return Response(
                AccountDetailSerializer(saved_data).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# api/accounts/balance/
class AccountBalanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="입출금 내역 조회",
        operation_description="유저의 입출금 내역을 확인할 수 있다.",
        request_body=None,
        responses={200: "내역 조회 성공"},
    )
    def get(self, request):
        user = request.user

        balance_list = Balance.objects.filter(user=user)

        serializer = BalanceListSerializer(balance_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id="입출금",
        operation_description="유저는 입출금 할 수 있다.",
        request_body=BalanceCreateSerializer,
        responses={
            201: "입출금 성공",
            400: "BAD REQUEST",
            403: "계좌 접근 불가능",
        },
    )
    def post(self, request):
        user = request.user
        change_balance = request.data.get("change_balance", None)
        account = request.data.get("account", None)

        if change_balance is None or change_balance == 0:
            return Response(
                {"message": "금액을 입력하세요."}, status=status.HTTP_400_BAD_REQUEST
            )

        if account is None:
            return Response(
                {"message": "입출금 계좌를 선택해주세요."}, status=status.HTTP_400_BAD_REQUEST
            )

        check_account = Account.objects.get(user=user).id
        if account != check_account:
            return Response(
                {"message": "해당 계좌에 접근할 수 없습니다."}, status=status.HTTP_403_FORBIDDEN
            )

        data = {"user": user.id, "account": account, "change_balance": change_balance}

        serializer = BalanceCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
