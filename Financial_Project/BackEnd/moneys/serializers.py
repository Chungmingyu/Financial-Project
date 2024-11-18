from rest_framework import serializers
from .models import DepositOption, DepositProduct, SavingOption, SavingProduct

        
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
        
     
    