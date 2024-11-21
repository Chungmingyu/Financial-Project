from django.urls import path
from . import views
from .views import UserDepositListCreateView, UserDepositDeleteView


app_name = 'moneys'
urlpatterns = [
    path('save-products/', views.save_products,
         name='save_products'),  # 예적금 데이터 저장
    path('deposit-products/', views.deposit_products,
         name='deposit_products'),  # 예금 조회
    path('saving-products/', views.saving_products,
         name='saving_products'),  # 적금 조회
    path('deposit-product-options/<str:fin_prdt_cd>/',
         views.deposit_product_options, name='deposit_product_options'),  # 예금 옵션 조회
    path('saving-product-options/<str:fin_prdt_cd>/',
         views.saving_product_options, name='saving_product_options'),  # 적금 옵션 조회
    path('deposit-products/top_rate/', views.top_rate, name='top_rate'),
    # 예금과 유저간 1:M URL
    path('deposits/', UserDepositListCreateView.as_view(),
         name='user-deposit-list-create'),
    path('deposits/<int:pk>/', UserDepositDeleteView.as_view(),
         name='user-deposit-delete'),
    # 예금 한건지 확인하는거
    path('check_subscription/<int:deposit_id>/',
         views.check_user_subscription, name='check_user_subscription'),
    path('stock_data/<str:symbol>/', views.stock_data, name='stock_data'),
    path('coin_data/', views.coin_data, name='coin_data'),
]
