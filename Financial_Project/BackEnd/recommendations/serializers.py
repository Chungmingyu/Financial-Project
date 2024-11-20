from rest_framework import serializers
from moneys.models import DepositOption, DepositProduct, SavingOption, SavingProduct
from .models import InvestmentPlan, PlanItem
        
class PlanItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanItem
        fields = ['product_type', 'product_id', 'amount', 'start_month', 'period']

class InvestmentPlanSerializer(serializers.ModelSerializer):
    items = PlanItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = InvestmentPlan
        fields = ['id', 'total_amount', 'investment_period', 'preferred_banks', 
                 'risk_preference', 'created_at', 'items']

class DepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = ['intr_rate_type', 'intr_rate_type_nm', 'save_trm', 
                 'intr_rate', 'intr_rate2']

class SavingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        fields = ['intr_rate_type', 'intr_rate_type_nm', 'rsrv_type',
                 'rsrv_type_nm', 'save_trm', 'intr_rate', 'intr_rate2']

class DepositProductSerializer(serializers.ModelSerializer):
    options = DepositOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = DepositProduct
        fields = ['fin_co_no', 'kor_co_nm', 'fin_prdt_cd', 'fin_prdt_nm',
                 'join_way', 'join_deny', 'options']

class SavingProductSerializer(serializers.ModelSerializer):
    options = SavingOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = SavingProduct
        fields = ['fin_co_no', 'kor_co_nm', 'fin_prdt_cd', 'fin_prdt_nm',
                 'join_way', 'join_deny', 'options']
    