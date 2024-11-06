from rest_framework import serializers
from .models import DepositOption, DepositProduct

class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = '__all__'
        
class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = '__all__'
        read_only_field = ('product',)
        

class DepositOptionsToprateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        exclude = ('product',)

         
        
class DepositProductsToprateSerializer(serializers.ModelSerializer):
    options = DepositOptionsToprateSerializer(many=True, read_only=True) 
    class Meta:
        model = DepositProduct
        fields = '__all__'

        
   
        
     
    