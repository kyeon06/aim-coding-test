from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from stocks.models import Stock
from stocks.serializers import StockCreateSerializer, StockListSerializer


# api/stocks/
class StockAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="증권 목록 조회",
        operation_description="등록된 증권 목록을 조회합니다.",
        request_body=None,
        responses={200: StockListSerializer},
    )
    def get(self, request):
        queryset = Stock.objects.all()
        serializer = StockListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id="증권 등록",
        operation_description="증권코드, 증권이름, 가격정보를 등록합니다.",
        request_body=StockCreateSerializer,
        responses={201: "증권 등록 성공", 400: "BAD REQUEST"},
    )
    def post(self, request):
        serializer = StockCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# api/stocks/<int:pk>/
class StockDetailAPIView(APIView):
    pass
