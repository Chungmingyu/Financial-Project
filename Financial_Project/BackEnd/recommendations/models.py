from django.db import models

# Create your models here.
class InvestmentPlan(models.Model):
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    investment_period = models.IntegerField()  # 개월 단위
    preferred_banks = models.TextField(null=True, blank=True)  # 쉼표로 구분된 은행 코드
    risk_preference = models.IntegerField()  # 1-5 척도
    created_at = models.DateTimeField(auto_now_add=True)

class PlanItem(models.Model):
    plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE, related_name='items')
    product_type = models.CharField(max_length=20)  # 'deposit' or 'saving'
    product_id = models.TextField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    start_month = models.IntegerField()  # 계획 시작부터 몇 개월 후
    period = models.IntegerField()  # 개월 단위
    expected_return = models.DecimalField(max_digits=15, decimal_places=2) 