from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import InvestmentPlan, PlanItem
from .services import InvestmentRecommender
from moneys.models import DepositProduct, SavingProduct
from .serializers import InvestmentPlanSerializer, DepositProductSerializer, SavingProductSerializer

class InvestmentPlanViewSet(viewsets.ModelViewSet):
    queryset = InvestmentPlan.objects.all()
    serializer_class = InvestmentPlanSerializer

    @action(detail=False, methods=['post'])
    def generate_plan(self, request):
        total_amount = float(request.data.get('total_amount'))
        period_months = int(request.data.get('period_months'))
        preferred_banks = request.data.get('preferred_banks')
        risk_preference = int(request.data.get('risk_preference', 3))

        recommender = InvestmentRecommender()
        recommender.train_model(
            DepositProduct.objects.all(),
            SavingProduct.objects.all()
        )

        plan_items = recommender.generate_investment_plan(
            total_amount,
            period_months,
            preferred_banks,
            risk_preference
        )

        # 계획 저장
        plan = InvestmentPlan.objects.create(
            total_amount=total_amount,
            investment_period=period_months,
            preferred_banks=preferred_banks,
            risk_preference=risk_preference
        )

        for item in plan_items:
            PlanItem.objects.create(plan=plan, **item)

        return Response({
            'plan_id': plan.id,
            'items': plan_items
        })

class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        product_ids = request.query_params.get('product_ids', '').split(',')
        
        deposit_products = DepositProduct.objects.filter(fin_prdt_cd__in=product_ids)
        saving_products = SavingProduct.objects.filter(fin_prdt_cd__in=product_ids)
        
        deposit_data = DepositProductSerializer(deposit_products, many=True).data
        saving_data = SavingProductSerializer(saving_products, many=True).data
        
        # 상품 타입 정보 추가
        for product in deposit_data:
            product['type'] = 'deposit'
        for product in saving_data:
            product['type'] = 'saving'
            
        return Response(deposit_data + saving_data)

class BankViewSet(viewsets.ViewSet):
    def list(self, request):
        # 고유한 은행 목록 조회
        deposit_banks = DepositProduct.objects.values('fin_co_no', 'kor_co_nm').distinct()
        saving_banks = SavingProduct.objects.values('fin_co_no', 'kor_co_nm').distinct()
        
        # 중복 제거 및 병합
        banks = {}
        for bank in deposit_banks:
            banks[bank['fin_co_no']] = {
                'code': bank['fin_co_no'],
                'name': bank['kor_co_nm']
            }
        for bank in saving_banks:
            banks[bank['fin_co_no']] = {
                'code': bank['fin_co_no'],
                'name': bank['kor_co_nm']
            }
            
        return Response(list(banks.values()))