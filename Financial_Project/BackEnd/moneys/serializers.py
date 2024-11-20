from rest_framework import serializers
from .models import DepositOption, DepositProduct, SavingOption, SavingProduct, UserDeposit


class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = '__all__'
        read_only_field = ('product',)


class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = '__all__'

    options = DepositOptionsSerializer(many=True, read_only=True)


class SavingOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        fields = '__all__'
        read_only_field = ('product',)


class SavingProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProduct
        fields = '__all__'

    options = SavingOptionsSerializer(many=True, read_only=True)


# 유저와 예금의 1:M 시리얼라이저
class DepositProductSerializer(serializers.ModelSerializer):
    # DepositProduct의 모든 정보 포함
    class Meta:
        model = DepositProduct
        fields = '__all__'

class UserDepositSerializer(serializers.ModelSerializer):
    deposit_product = DepositProductSerializer()

    class Meta:
        model = UserDeposit
        fields = ['id', 'user', 'deposit_product', 'amount', 'date_created']

