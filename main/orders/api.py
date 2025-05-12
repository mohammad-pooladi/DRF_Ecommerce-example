from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from main.api.mixins import ApiAuthMixin
from main.orders.models import Order, OrderItem
from main.products.models import Products
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from main.api.pagination import LimitOffsetPagination


class OrderAPI(ApiAuthMixin, APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class OrderSerializer(serializers.ModelSerializer):
        class Meta:
            model = Order
            fields = ("id", "status", "total_price")

    @extend_schema(responses={200: OrderSerializer(many=True)})
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        paginator = self.Pagination()
        paginated_orders = paginator.paginate_queryset(orders, request)
        serializer = self.OrderSerializer(paginated_orders, many=True)
        return paginator.get_paginated_response(serializer.data)


class OrderItemAPI(ApiAuthMixin, APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class ProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = Products
            fields = ("id", "name", "price")

    class OrderItemSerializer(serializers.ModelSerializer):
        products = ProductSerializer()

        class Meta:
            model = OrderItem
            fields = ("id", "products", "quantity", "price")

    @extend_schema(responses={200: OrderItemSerializer(many=True)})
    def get(self, request):
        order_id = request.query_params.get("order_id")
        if not order_id:
            return Response(
                {"detail": "order_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        order = get_object_or_404(Order, id=order_id, user=request.user)
        items = order.items.all()
        paginator = self.Pagination()
        paginated_items = paginator.paginate_queryset(items, request)
        serializer = self.OrderItemSerializer(paginated_items, many=True)
        return paginator.get_paginated_response(serializer.data)
