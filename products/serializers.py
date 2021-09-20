from rest_framework import serializers
from products.models import Product
from django.contrib.auth import get_user_model


class ProductCreateSerializer(serializers.ModelSerializer):
    productName = serializers.CharField(required=True)
    cost = serializers.IntegerField(required=True)
    amountAvailable = serializers.IntegerField(required=True)

    class Meta:
        model = Product
        fields = ('productName', 'cost', 'amountAvailable')

    def create(self, validated_data):
        prod = Product.objects.create(**validated_data)
        return prod


class ProductDeleteSerializer(serializers.ModelSerializer):
    productName = serializers.CharField(required=True)

    class Meta:
        model = Product
        fields = ('productName',)


class ProductUpdateSerializer(serializers.ModelSerializer):
    productName = serializers.CharField(required=True)
    cost = serializers.IntegerField(required=True)
    amountAvailable = serializers.IntegerField(required=True)

    class Meta:
        model = Product
        fields = ('productName', 'cost', 'amountAvailable')


class ProductBuySerializer(serializers.ModelSerializer):
    productName = serializers.CharField(required=True)
    quantity = serializers.IntegerField(required=True)
    sellerId = serializers.CharField(required=True)

    class Meta:
        model = Product
        fields = ('productName', 'quantity', 'sellerId')