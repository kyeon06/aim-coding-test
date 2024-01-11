from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from accounts.models import Account

from portfolio.serializers import PortfolioAdviceSerializer


class PortfolioAdviceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="포트폴리오 자문 요청",
        operation_description="유형을 선택하여 자문 요청 할 수 있다. (TYPE-1/TYPE-2)",
        request_body=PortfolioAdviceSerializer,
        responses={200: "자문 요청 성공", 404: "NOT FOUND"},
    )
    def post(self, request):
        user = request.user
        risk_type = request.data.get("risk_type")

        data = {"type": risk_type, "message": "자문 요청"}

        try:
            user_balance = Account.objects.get(user=user).balance
        except:
            return Response(
                {"message": "잔고를 확인할 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )

        if risk_type == "TYPE-1":
            data["description"] = "유형1) 잔고를 최대한 많이 사용하는 포트폴리오 유형 (잔고가 거의 남아 있지 않게 된다.)"
            data["data"] = {"use_balance": user_balance}
        elif risk_type == "TYPE-2":
            data["description"] = "유형2) 잔고를 중간정도 사용하는 포트폴리오 유형 (원화 잔고가 반쯤 남아 있게 된다.)"
            data["data"] = {"use_balance": user_balance // 2}

        return Response(data, status=status.HTTP_200_OK)
