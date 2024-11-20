from django.urls import path
from .views import InvestmentPlanViewSet, ProductViewSet, BankViewSet

urlpatterns = [
    path('investment-plans/',
         InvestmentPlanViewSet.as_view({'post': 'generate_plan'})),
    path('products/', ProductViewSet.as_view({'get': 'list'})),
    path('banks/', BankViewSet.as_view({'get': 'list'})),
]
