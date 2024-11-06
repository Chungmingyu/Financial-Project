from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view
from .models import DepositOption, DepositProduct
from .serializers import DepositOptionsSerializer, DepositProductsSerializer, DepositProductsToprateSerializer
from rest_framework.response import Response
import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from pprint import pprint
# Create your views here.

@api_view(['GET'])
def save_deposit_products(request):
    api_key = settings.API_KEY
    
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(url).json()
    
    # pprint(response['result']['optionList'])
    
    for li in response['result']['baseList']:
        fin_prdt_cd = li.get('fin_prdt_cd', -1)
        kor_co_nm = li.get('kor_co_nm', -1)
        fin_prdt_nm = li.get('fin_prdt_nm', -1)
        etc_note = li.get('etc_note', -1)
        join_deny = li.get('join_deny', -1)
        join_member = li.get('join_member', -1)
        join_way = li.get('join_way', -1)
        spcl_cnd = li.get('spcl_cnd', -1)
        
        if DepositProduct.objects.filter(fin_prdt_cd=fin_prdt_cd, kor_co_nm=kor_co_nm, fin_prdt_nm=fin_prdt_nm, etc_note=etc_note, join_deny=join_deny, join_member=join_member, join_way=join_way, spcl_cnd=spcl_cnd).exists():
            continue
        
        save_data = {
            'fin_prdt_cd':fin_prdt_cd,
            'kor_co_nm':kor_co_nm,
            'fin_prdt_nm':fin_prdt_nm,
            'etc_note':etc_note,
            'join_deny':join_deny,
            'join_member':join_member,
            'join_way':join_way,
            'spcl_cnd':spcl_cnd,
        }
    
        serializer = DepositProductsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
    for optionli in response['result']['optionList']:
        fin_prdt_cd = optionli.get('fin_prdt_cd', -1)
        product, created = DepositProduct.objects.get_or_create(fin_prdt_cd=fin_prdt_cd)
        intr_rate_type_nm = optionli.get('intr_rate_type_nm', -1)
        intr_rate = optionli.get('intr_rate', -1)
        intr_rate2 = optionli.get('intr_rate2', -1)
        save_trm = optionli.get('save_trm', -1)

        # if intr_rate is None or intr_rate_type_nm is None or save_trm is None:
        #     continue
        
        if DepositOption.objects.filter(product=product, intr_rate_type_nm=intr_rate_type_nm, intr_rate=intr_rate, intr_rate2=intr_rate2, save_trm=save_trm).exists():
            continue
        
        save_data = {
            'product':product.id,
            'fin_prdt_cd':fin_prdt_cd,
            'intr_rate_type_nm':intr_rate_type_nm,
            'intr_rate':intr_rate,
            'intr_rate2':intr_rate2,
            'save_trm':save_trm,
        }
    
        serializer = DepositOptionsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    
    return JsonResponse({'message':'저장 성공!'})

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

@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    options = DepositOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = DepositOptionsSerializer(options, many=True)
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