from rest_framework import serializers
from products.models import Product


class ProductCreateSerializer(serializers.ModelSerializer):
    productName = serializers.CharField(required=True)
    cost = serializers.IntegerField(required=True)
    amountAvailable = serializers.IntegerField(required=True)

    class Meta:
        model = Product
        fields = ('productName', 'cost', 'amountAvailable')

    def validate(self, data):
        cost = data['cost']
        quantity = data['amountAvailable']
        if quantity < 1 or cost < 1:
            raise serializers.ValidationError('Quantity/Cost should be at least 1', code=400)
        return data

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

    def validate(self, data):
        cost = data['cost']
        quantity = data['amountAvailable']
        if quantity < 1 or cost < 1:
            raise serializers.ValidationError('Quantity/Cost should be at least 1', code=400)

        return data


class ProductBuySerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(required=True)

    class Meta:
        model = Product
        fields = ('quantity',)
        read_only_fields = ('productName', 'sellerId')

    def validate(self, data):
        quantity = data['quantity']
        if quantity < 1:
            raise serializers.ValidationError('Quantity should be at least 1', code=400)

        return data
