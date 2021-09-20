from rest_framework import serializers
from users.models import User, Deposit


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserPwdChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'confirm_password')
        extra_kwargs = {'old_password': {'write_only': True},
                        'new_password': {'write_only': True},
                        'confirm_password': {'write_only': True}
                        }


class DepositSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(required=True)
    class Meta:
        model = Deposit
        fields = ('amount',)


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

