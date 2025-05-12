from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from main.api.mixins import ApiAuthMixin
from main.api.pagination import LimitOffsetPagination
from .models import Products, Category


class CategoryAPI(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class CategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ["id", "name", "slug"]

    @extend_schema(
        request=CategorySerializer,
        responses={
            200: CategorySerializer(many=True),
            201: CategorySerializer,
            400: "Bad Request",
        },
    )
    def post(self, request):
        serializer = self.CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses=CategorySerializer(many=True)
    )
    def get(self, request):
        categoriys = Category.objects.all()
        paginator = self.Pagination()
        result = paginator.paginate_queryset(categoriys, request)
        serializer = self.CategorySerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)


class ProductAPI(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class ProductsSerializer(serializers.ModelSerializer):
        class Meta:
            model = Products
            fields = [
                "id",
                "name",
                "slug",
                "description",
                "categore",
                "price",
                "stock",
                "image",
            ]

    @extend_schema(
        request=ProductsSerializer,
        responses={
            200: ProductsSerializer(many=True),
            201: ProductsSerializer,
            400: "Bad Request",
        },
    )
    def post(self, request):
        serializer = self.ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses=ProductsSerializer(many=True)
    )
    def get(self, request):
        products = Products.objects.all()
        paginator = self.Pagination()
        result = paginator.paginate_queryset(products, request)
        serializer = self.ProductsSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)
