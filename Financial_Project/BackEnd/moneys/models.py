from django.db import models

class DepositProduct(models.Model):
    dcls_month = models.TextField() # 공시 제출월 [YYYYMM]
    fin_co_no = models.TextField() # 금융회사 코드
    kor_co_nm = models.TextField() # 금융회사 명
    fin_prdt_cd = models.TextField(unique=True) # 금융상품 코드
    fin_prdt_nm = models.TextField() # 금융 상품명
    join_way = models.TextField() # 가입 방법
    mtrt_int = models.TextField() # 만기 후 이자율
    spcl_cnd = models.TextField() # 우대조건
    join_deny = models.IntegerField(default=0, null=True, blank=True) # 가입제한Ex) 1:제한없음, 2:서민전용, 3:일부제한
    join_member = models.TextField() # 가입대상
    etc_note = models.TextField() # 기타 유의사항
    max_limit = models.TextField(default='없음', null=True, blank=True) # 최고한도
    dcls_strt_day = models.TextField() # 공시 시작일
    dcls_end_day = models.TextField(default='없음', null=True, blank=True) # 공시 종료일
    fin_co_subm_day = models.TextField() # 금융회사 제출일 [YYYYMMDDHH24MI]

class DepositOption(models.Model):
    product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE, related_name='options')
    fin_prdt_cd = models.TextField() # 금융상품 코드
    intr_rate_type = models.TextField() # 저축 금리 유형
    intr_rate_type_nm = models.CharField(max_length=100) # 저축 금리 유형명
    save_trm = models.IntegerField() # 저축 기간 [단위: 개월]
    intr_rate = models.FloatField(null=True, blank=True) # 저축 금리 [소수점 2자리]
    intr_rate2 = models.FloatField(null=True, blank=True) # 최고 우대금리 [소수점 2자리]
    
class SavingProduct(models.Model):
    dcls_month = models.TextField() # 공시 제출월 [YYYYMM]
    fin_co_no = models.TextField() # 금융회사 코드
    kor_co_nm = models.TextField() # 금융회사 명
    fin_prdt_cd = models.TextField(unique=True) # 금융상품 코드
    fin_prdt_nm = models.TextField() # 금융 상품명
    join_way = models.TextField() # 가입 방법
    mtrt_int = models.TextField() # 만기 후 이자율
    spcl_cnd = models.TextField() # 우대조건
    join_deny = models.IntegerField(default=0, null=True, blank=True) # 가입제한Ex) 1:제한없음, 2:서민전용, 3:일부제한
    join_member = models.TextField() # 가입대상
    etc_note = models.TextField() # 기타 유의사항
    max_limit = models.TextField(default='없음', null=True, blank=True) # 최고한도
    dcls_strt_day = models.TextField() # 공시 시작일
    dcls_end_day = models.TextField(default='없음', null=True, blank=True) # 공시 종료일
    fin_co_subm_day = models.TextField() # 금융회사 제출일 [YYYYMMDDHH24MI]

class SavingOption(models.Model):
    product = models.ForeignKey(SavingProduct, on_delete=models.CASCADE, related_name='options')
    fin_prdt_cd = models.TextField() # 금융상품 코드
    intr_rate_type = models.TextField() # 저축 금리 유형
    intr_rate_type_nm = models.CharField(max_length=100) # 저축 금리 유형명
    rsrv_type = models.TextField() # 적립 유형
    rsrv_type_nm = models.TextField() # 적립 유형명
    save_trm = models.IntegerField() # 저축 기간 [단위: 개월]
    intr_rate = models.FloatField(null=True, blank=True) # 저축 금리 [소수점 2자리]
    intr_rate2 = models.FloatField(null=True, blank=True) # 최고 우대금리 [소수점 2자리]
    