from django.urls import path
from . import views

app_name = 'moneys'
urlpatterns = [
    path('save-products/', views.save_products, name='save_products'), # 예적금 데이터 저장
    path('deposit-products/', views.deposit_products, name='deposit_products'), # 예금 조회
    path('saving-products/', views.saving_products, name='saving_products'), # 적금 조회
    path('deposit-product-options/<str:fin_prdt_cd>/', views.deposit_product_options, name='deposit_product_options'), # 예금 옵션 조회
    path('saving-product-options/<str:fin_prdt_cd>/', views.saving_product_options, name='saving_product_options'), # 적금 옵션 조회
    path('deposit-products/top_rate/', views.top_rate, name='top_rate'),
]
