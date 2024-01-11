from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from stocks.models import Stock
from stocks.serializers import (
    StockCreateSerializer,
    StockDetailSerializer,
    StockListSerializer,
    StockUpdateSerializer,
)


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
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="증권 정보 조회",
        operation_description="증권 정보를 조회할 수 있다.",
        request_body=None,
        responses={200: "조회 성공", 404: "NOT FOUND"},
    )
    def get(self, request, pk):
        try:
            data = Stock.objects.get(pk=pk)
        except:
            return Response(
                {"message": "관련된 정보가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = StockDetailSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id="증권 정보 수정",
        operation_description="증권 정보를 수정할 수 있다.",
        request_body=StockUpdateSerializer,
        responses={200: StockDetailSerializer, 400: "BAD REQUEST", 404: "NOT FOUND"},
    )
    def put(self, request, pk):
        update_data = request.data

        try:
            data = Stock.objects.get(pk=pk)
        except:
            return Response(
                {"message": "관련된 정보가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = StockDetailSerializer(data, data=update_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_id="증권 정보 삭제",
        operation_description="증권 정보를 삭제할 수 있다.",
        request_body=None,
        responses={200: "삭제 완료", 404: "NOT FOUND"},
    )
    def delete(self, request, pk):
        try:
            data = Stock.objects.get(pk=pk)
        except:
            return Response(
                {"message": "해당 증권 정보를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )
        data.delete()
        return Response({"message": "증권 정보 삭제 완료"}, status=status.HTTP_200_OK)
