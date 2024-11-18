from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view
from .models import DepositOption, DepositProduct, SavingProduct, SavingOption
from .serializers import DepositOptionsSerializer, DepositProductsSerializer, SavingOptionsSerializer, SavingProductsSerializer
from rest_framework.response import Response
import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from pprint import pprint
# Create your views here.

@api_view(['GET'])
def save_products(request):
    api_key = settings.DEPOSIT_API_KEY
    topFinGrpNo = '020000' # 금융회사가 속한 권역 코드 Ex) 020000(은행), 030200(여신전문), 030300(저축은행), 050000(보험), 060000(금융투자)
    pageNo = '1' # 조회하고자 하는 페이지 번호 Ex) 1, 2, 3
    financeCd = '' # 금융회사 코드 또는 명 Ex) 0010587, 0010588, 0010722, 국민, 상호, 하나

    deposit_url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=2'
    saving_url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    deposit_response = requests.get(deposit_url).json()
    saving_response = requests.get(saving_url).json()
    # pprint(response['result']['optionList'])
    
    # 예금 상품 저장
    for li in deposit_response['result']['baseList']:
        dcls_month = li.get('dcls_month')
        fin_co_no = li.get('fin_co_no')
        kor_co_nm = li.get('kor_co_nm')
        fin_prdt_cd = li.get('fin_prdt_cd')
        fin_prdt_nm = li.get('fin_prdt_nm')
        join_way = li.get('join_way')
        mtrt_int = li.get('mtrt_int')
        spcl_cnd = li.get('spcl_cnd')
        join_deny = li.get('join_deny') or 0
        join_member = li.get('join_member')
        etc_note = li.get('etc_note')
        max_limit = li.get('max_limit') or '없음' # 최고한도
        dcls_strt_day = li.get('dcls_strt_day')  # 공시 시작일
        dcls_end_day = li.get('dcls_end_day') or '없음'  # 공시 종료일
        fin_co_subm_day = li.get('fin_co_subm_day')  # 금융회사 제출일

        if DepositProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            continue
        
        save_data = {
            'fin_prdt_cd': fin_prdt_cd,
            'kor_co_nm': kor_co_nm,
            'dcls_month':dcls_month,
            'fin_co_no':fin_co_no,
            'mtrt_int':mtrt_int,
            'fin_prdt_nm': fin_prdt_nm,
            'etc_note': etc_note,
            'join_deny': join_deny,
            'join_member': join_member,
            'join_way': join_way,
            'spcl_cnd': spcl_cnd,
            'max_limit': max_limit,
            'dcls_strt_day': dcls_strt_day,
            'dcls_end_day': dcls_end_day,
            'fin_co_subm_day': fin_co_subm_day,
        }
    
        serializer = DepositProductsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    # 적금 상품 저장
    for li in saving_response['result']['baseList']:
        dcls_month = li.get('dcls_month')
        fin_co_no = li.get('fin_co_no')
        kor_co_nm = li.get('kor_co_nm')
        fin_prdt_cd = li.get('fin_prdt_cd')
        fin_prdt_nm = li.get('fin_prdt_nm')
        join_way = li.get('join_way')
        mtrt_int = li.get('mtrt_int')
        spcl_cnd = li.get('spcl_cnd')
        join_deny = li.get('join_deny') or 0
        join_member = li.get('join_member')
        etc_note = li.get('etc_note')
        max_limit = li.get('max_limit') or '없음'  # 최고한도
        dcls_strt_day = li.get('dcls_strt_day')  # 공시 시작일
        dcls_end_day = li.get('dcls_end_day') or '없음'  # 공시 종료일
        fin_co_subm_day = li.get('fin_co_subm_day')  # 금융회사 제출일

        if SavingProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            continue
        
        save_data = {
            'fin_prdt_cd': fin_prdt_cd,
            'kor_co_nm': kor_co_nm,
            'dcls_month':dcls_month,
            'fin_co_no':fin_co_no,
            'mtrt_int':mtrt_int,
            'fin_prdt_nm': fin_prdt_nm,
            'etc_note': etc_note,
            'join_deny': join_deny,
            'join_member': join_member,
            'join_way': join_way,
            'spcl_cnd': spcl_cnd,
            'max_limit': max_limit,
            'dcls_strt_day': dcls_strt_day,
            'dcls_end_day': dcls_end_day,
            'fin_co_subm_day': fin_co_subm_day,
        }
    
        serializer = SavingProductsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    # 예금 옵션 저장
    for optionli in deposit_response['result']['optionList']:
        fin_prdt_cd = optionli.get('fin_prdt_cd', -1)
        product, created = DepositProduct.objects.get_or_create(fin_prdt_cd=fin_prdt_cd)
        intr_rate_type = optionli.get('intr_rate_type', -1)
        intr_rate_type_nm = optionli.get('intr_rate_type_nm', -1)
        save_trm = optionli.get('save_trm', -1)
        intr_rate2 = optionli.get('intr_rate2', -1)
        intr_rate = optionli.get('intr_rate', -1)

        
        # 중복된 데이터는 저장하지 않음
        if DepositOption.objects.filter(product=product, intr_rate_type_nm=intr_rate_type_nm, intr_rate=intr_rate, intr_rate2=intr_rate2, save_trm=save_trm).exists():
            continue
        
        save_data = {
            'product': product.id,
            'fin_prdt_cd': fin_prdt_cd,
            'intr_rate_type':intr_rate_type,
            'intr_rate_type_nm': intr_rate_type_nm,
            'intr_rate': intr_rate,
            'intr_rate2': intr_rate2,
            'save_trm': save_trm,
        }
    
        serializer = DepositOptionsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        
    # 적금 옵션 저장
    for optionli in saving_response['result']['optionList']:
        fin_prdt_cd = optionli.get('fin_prdt_cd')
        product, created = SavingProduct.objects.get_or_create(fin_prdt_cd=fin_prdt_cd)
        intr_rate_type = optionli.get('intr_rate_type')
        intr_rate_type_nm = optionli.get('intr_rate_type_nm')
        rsrv_type = optionli.get('rsrv_type')
        rsrv_type_nm = optionli.get('rsrv_type_nm')
        save_trm = optionli.get('save_trm')
        intr_rate2 = optionli.get('intr_rate2')
        intr_rate = optionli.get('intr_rate')

        
        # 중복된 데이터는 저장하지 않음
        if SavingOption.objects.filter(product=product, intr_rate_type_nm=intr_rate_type_nm, intr_rate=intr_rate, intr_rate2=intr_rate2, save_trm=save_trm).exists():
            continue
        
        save_data = {
            'product': product.id,
            'fin_prdt_cd': fin_prdt_cd,
            'intr_rate_type':intr_rate_type,
            'intr_rate_type_nm': intr_rate_type_nm,
            'intr_rate': intr_rate,
            'intr_rate2': intr_rate2,
            'save_trm': save_trm,
            'rsrv_type':rsrv_type,
            'rsrv_type_nm': rsrv_type_nm
        }
    
        serializer = SavingOptionsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    
    return JsonResponse({'message':'저장 성공!'})

# 예금 정보 생성 및 조회
@api_view(['GET', 'POST'])
def deposit_products(request):
    if request.method == 'GET':
        products = DepositProduct.objects.all()
        serializer = DepositProductsSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# 적금 정보 생성 및 조회
@api_view(['GET', 'POST'])
def saving_products(request):
    if request.method == 'GET':
        products = SavingProduct.objects.all()
        serializer = SavingProductsSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SavingProductsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# 예금 옵션 조회
@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    options = DepositOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = DepositOptionsSerializer(options, many=True)
    return Response(serializer.data)

# 적금 옵션 조회
@api_view(['GET'])
def saving_product_options(request, fin_prdt_cd):
    options = SavingOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = SavingOptionsSerializer(options, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def top_rate(request):
    option = DepositOption.objects.order_by('-intr_rate2').first()
    product = option.product
    product_serializer = DepositProductsSerializer(product)
    option_serializer = DepositOptionsSerializer(option)
    return Response({
        'deposit_product':product_serializer.data,
        'option':option_serializer.data,
    })