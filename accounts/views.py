from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from accounts.models import Account
from accounts.serializers import AccountDetailSerializer, AccountSerializer


# api/accounts/
class AccountAPIView(APIView):
    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(
        operation_id="계좌 잔고 조회",
        operation_description="보유하고 있는 계좌의 잔고를 확인할 수 있다.",
        request_body=None,
        responses={
            200 : AccountDetailSerializer,
            401 : "Unauthenticated",
            404 : "Not Found",
        }
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
            201 : AccountDetailSerializer,
            401 : "Unauthenticated",
            400 : "계좌가 이미 존재할 경우 OR 잘못된 요청청",
        }
    )
    def post(self, request):
        user = request.user

        is_exists = Account.objects.filter(user=user).exists()
        if is_exists:
            return Response(
                {"message": "계좌가 이미 존재합니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            "user" : user.id
        }

        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            saved_data = serializer.save()
            return Response(
                AccountDetailSerializer(saved_data).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountBalanceAPIView(APIView):
    pass
