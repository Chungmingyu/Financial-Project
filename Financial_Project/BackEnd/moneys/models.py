from django.conf import settings
from django.db import models


class DepositProduct(models.Model):
    id = models.AutoField(primary_key=True)
    dcls_month = models.TextField()  # 공시 제출월 [YYYYMM]
    fin_co_no = models.TextField()  # 금융회사 코드
    kor_co_nm = models.TextField()  # 금융회사 명
    fin_prdt_cd = models.TextField(unique=True)  # 금융상품 코드
    fin_prdt_nm = models.TextField()  # 금융 상품명
    join_way = models.TextField()  # 가입 방법
    mtrt_int = models.TextField()  # 만기 후 이자율
    spcl_cnd = models.TextField()  # 우대조건
    # 가입제한Ex) 1:제한없음, 2:서민전용, 3:일부제한
    join_deny = models.IntegerField(default=0, null=True, blank=True)
    join_member = models.TextField()  # 가입대상
    etc_note = models.TextField()  # 기타 유의사항
    max_limit = models.TextField(default='없음', null=True, blank=True)  # 최고한도
    dcls_strt_day = models.TextField()  # 공시 시작일
    dcls_end_day = models.TextField(
        default='없음', null=True, blank=True)  # 공시 종료일
    fin_co_subm_day = models.TextField()  # 금융회사 제출일 [YYYYMMDDHH24MI]

    def __str__(self):
        return self.fin_prdt_nm  # 금융 상품명 반환


class DepositOption(models.Model):
    product = models.ForeignKey(
        DepositProduct, on_delete=models.CASCADE, related_name='options')
    fin_prdt_cd = models.TextField()  # 금융상품 코드
    intr_rate_type = models.TextField()  # 저축 금리 유형
    intr_rate_type_nm = models.CharField(max_length=100)  # 저축 금리 유형명
    save_trm = models.IntegerField()  # 저축 기간 [단위: 개월]
    intr_rate = models.FloatField(null=True, blank=True)  # 저축 금리 [소수점 2자리]
    intr_rate2 = models.FloatField(null=True, blank=True)  # 최고 우대금리 [소수점 2자리]


class SavingProduct(models.Model):
    dcls_month = models.TextField()  # 공시 제출월 [YYYYMM]
    fin_co_no = models.TextField()  # 금융회사 코드
    kor_co_nm = models.TextField()  # 금융회사 명
    fin_prdt_cd = models.TextField(unique=True)  # 금융상품 코드
    fin_prdt_nm = models.TextField()  # 금융 상품명
    join_way = models.TextField()  # 가입 방법
    mtrt_int = models.TextField()  # 만기 후 이자율
    spcl_cnd = models.TextField()  # 우대조건
    # 가입제한Ex) 1:제한없음, 2:서민전용, 3:일부제한
    join_deny = models.IntegerField(default=0, null=True, blank=True)
    join_member = models.TextField()  # 가입대상
    etc_note = models.TextField()  # 기타 유의사항
    max_limit = models.TextField(default='없음', null=True, blank=True)  # 최고한도
    dcls_strt_day = models.TextField()  # 공시 시작일
    dcls_end_day = models.TextField(
        default='없음', null=True, blank=True)  # 공시 종료일
    fin_co_subm_day = models.TextField()  # 금융회사 제출일 [YYYYMMDDHH24MI]


class SavingOption(models.Model):
    product = models.ForeignKey(
        SavingProduct, on_delete=models.CASCADE, related_name='options')
    fin_prdt_cd = models.TextField()  # 금융상품 코드
    intr_rate_type = models.TextField()  # 저축 금리 유형
    intr_rate_type_nm = models.CharField(max_length=100)  # 저축 금리 유형명
    rsrv_type = models.TextField()  # 적립 유형
    rsrv_type_nm = models.TextField()  # 적립 유형명
    save_trm = models.IntegerField()  # 저축 기간 [단위: 개월]
    intr_rate = models.FloatField(null=True, blank=True)  # 저축 금리 [소수점 2자리]
    intr_rate2 = models.FloatField(null=True, blank=True)  # 최고 우대금리 [소수점 2자리]


Usermodel = settings.AUTH_USER_MODEL


class UserDeposit(models.Model):
    user = models.ForeignKey(
        Usermodel, on_delete=models.CASCADE, related_name="deposits"
    )  # 1:M 관계 설정
    deposit_product = models.ForeignKey(
        DepositProduct, on_delete=models.CASCADE
    )  # 1:M 관계 설정
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # 예금 금액
    date_created = models.DateTimeField(auto_now_add=True)  # 예금 생성일

    def __str__(self):
        # 상품명 출력
        return f'{self.user.username} - {self.deposit_product.fin_prdt_nm}'


class UserSaving(models.Model):
    user = models.ForeignKey(
        Usermodel, on_delete=models.CASCADE, related_name="savings")
    saving_product = models.ForeignKey(SavingProduct, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
