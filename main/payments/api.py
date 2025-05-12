from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from main.api.mixins import ApiAuthMixin
from .models import Address, Payment
from django.db import transaction
from drf_spectacular.utils import extend_schema


class AddressAPI(ApiAuthMixin, APIView):
    class AddressSerializer(serializers.ModelSerializer):
        class Meta:
            model = Address
            fields = (
                "country",
                "province",
                "city",
                "street",
                "house_number",
                "postal_code",
                "phone_number",
                "is_default",
            )

    @extend_schema(
        request=AddressSerializer,
        responses={201: AddressSerializer, 400: "Bad Request"},
    )
    def post(self, request):
        serializer = self.AddressSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: AddressSerializer(many=True)},
    )
    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        serializer = self.AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentsAPI(ApiAuthMixin, APIView):
    class AddressNestedSerializer(serializers.ModelSerializer):
        class Meta:
            model = Address
            fields = (
                "country",
                "province",
                "city",
                "street",
                "house_number",
                "postal_code",
                "phone_number",
                "is_default",
            )

    class PaymentsSerializer(serializers.ModelSerializer):
        address = AddressNestedSerializer(context={"request": request})
        payment_method = serializers.ChoiceField(choices=[("crypto", "Crypto")])
        status = serializers.ChoiceField(choices=Payment.STATUS_CHOICES)
        user = serializers.HiddenField(default=serializers.CurrentUserDefault())

        class Meta:
            model = Payment
            fields = (
                "user",
                "order",
                "amount",
                "transaction_id",
                "payment_method",
                "status",
                "address",
            )

        def create(self, validated_data):
            address_data = validated_data.pop("address")
            user = validated_data["user"]
            address = Address.objects.create(user=user, **address_data)
            payment = Payment.objects.create(address=address, **validated_data)
            return payment

    @extend_schema(
        request=PaymentsSerializer,
        responses={201: PaymentsSerializer, 400: "Bad Request"},
    )
    def post(self, request):
        serializer = self.PaymentsSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            with transaction.atomic():
                payment = serializer.save()
                return Response(self.PaymentsSerializer(payment, context={"request": request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: PaymentsSerializer(many=True)},
    )
    def get(self, request):
        payments = Payment.objects.filter(user=request.user)
        serializer = self.PaymentsSerializer(payments, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
