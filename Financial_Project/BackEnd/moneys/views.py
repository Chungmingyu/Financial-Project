from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view
from .models import DepositOption, DepositProduct, SavingProduct, SavingOption, UserDeposit
from .serializers import DepositOptionsSerializer, DepositProductsSerializer, SavingOptionsSerializer, SavingProductsSerializer, UserDepositSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from pprint import pprint
from rest_framework import generics
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserDeposit, DepositProduct, Apartment
from .serializers import UserDepositSerializer
from django.conf import settings
from rest_framework.exceptions import ValidationError
from django.http import JsonResponse


def home_data(request):
    api_key = settings.HOME_API_KEY
    house_types = {
        'house': {'id': 'A_2024_00025', 'name': '주택종합'},
        'apartment': {'id': 'A_2024_00060', 'name': '아파트'},
        'row_house': {'id': 'A_2024_00095', 'name': '연립/다세대'},
        'single_house': {'id': 'A_2024_00128', 'name': '단독주택'}
    }

    # URL 파라미터로 주택 유형 받기
    house_type = request.GET.get('type', 'apartment')  # 기본값은 아파트
    if house_type not in house_types:
        return JsonResponse({'error': '잘못된 주택 유형'}, status=400)

    saved_data = []
    url = f'https://www.reb.or.kr/r-one/openapi/SttsApiTblData.do?KEY={api_key}&STATBL_ID={house_types[house_type]["id"]}&DTACYCLE_CD=MM&Type=json&pIndex=1&pSize=1000&START_WRTTIME=202410'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rows = data.get('SttsApiTblData', [])[1].get('row', [])

        for row in rows:
            location = row.get('CLS_NM')
            location_full = row.get('CLS_FULLNM')
            price = row.get('DTA_VAL')

            if location and price:
                saved_data.append({
                    'type': house_types[house_type]['name'],
                    'location': location,
                    'location_full': location_full,
                    'price': float(price)
                })

        return JsonResponse({
            'message': '데이터를 성공적으로 불러왔습니다.',
            'type': house_types[house_type]['name'],
            'data': saved_data
        })

    except requests.RequestException as e:
        return JsonResponse({'error': f'API 요청 실패: {str(e)}'}, status=500)


def stock_data(request, symbol):
    api_key = settings.FINNHUB_API_KEY
    search_url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}'
    search_response = requests.get(search_url)
    # 응답 상태 코드 확인
    if search_response.status_code != 200:
        return JsonResponse({'error': f"API 요청 실패: {search_response.status_code}"}, status=400)

    quote_data = search_response.json()

    if 'error' in quote_data:
        return JsonResponse({'error': 'Finnhub API 응답 오류'}, status=400)

    stock_data = {
        'symbol': symbol,
        'quote': quote_data,
    }
    return JsonResponse(stock_data)


def coin_data(request):
    api_key = settings.UPBIT_API_KEY
    secret_key = settings.UPBIT_SECRET_KEY
    # 마켓 정보 가져오기
    market_url = 'https://api.upbit.com/v1/market/all'
    market_response = requests.get(market_url)

    if market_response.status_code != 200:
        return JsonResponse({'error': f"마켓 정보 API 요청 실패: {market_response.status_code}"}, status=400)

    market_data = market_response.json()
    market_info = {item['market']: item['korean_name'] for item in market_data}

    # 가격 정보 가져오기
    ticker_url = 'https://api.upbit.com/v1/ticker/all'
    params = {
        'quote_currencies': "KRW"  # 예: KRW-BTC
    }
    price_response = requests.get(ticker_url, params=params)

    if price_response.status_code != 200:
        return JsonResponse({'error': f"가격 정보 API 요청 실패: {price_response.status_code}"}, status=400)

    price_data = price_response.json()

    # 응답 데이터 구성
    response_data = []
    for ticker in price_data:
        market = ticker['market']
        response_data.append({
            'market': market,
            'korean_name': market_info.get(market, ''),
            'current_price': ticker['trade_price'],
            'change_rate': ticker['signed_change_rate'] * 100,  # 백분율로 변환
            'change_price': ticker['signed_change_price'],
            'high_price': ticker['high_price'],
            'low_price': ticker['low_price'],
            'acc_trade_volume_24h': ticker['acc_trade_volume_24h']
        })

    return JsonResponse({'data': response_data})


# 예금 추가 한건지 확인하는거
@api_view(['GET'])
def check_user_subscription(request, deposit_id):
    # 로그인된 유저 확인
    user = request.user
    # 해당 유저가 해당 예금 상품에 가입했는지 확인
    if DepositProduct.objects.filter(id=deposit_id, user=user).exists():
        return Response({"subscribed": True}, status=status.HTTP_200_OK)
    return Response({"subscribed": False}, status=status.HTTP_200_OK)

# 예금 추가


class UserDepositListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        deposits = UserDeposit.objects.filter(user=user)
        serializer = UserDepositSerializer(deposits, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        deposit_product_id = request.data.get("deposit_product")
        amount = request.data.get("amount")

        if not deposit_product_id or not amount:
            return Response({"error": "Deposit product and amount are required."}, status=400)

        try:
            deposit_product = DepositProduct.objects.get(id=deposit_product_id)
        except DepositProduct.DoesNotExist:
            return Response({"error": "Deposit product not found."}, status=404)

        # 이미 해당 사용자와 해당 예금 상품에 대한 UserDeposit이 존재하는지 확인
        if UserDeposit.objects.filter(user=request.user, deposit_product=deposit_product).exists():
            return Response({"error": "이미 가입되어있습니다."}, status=400)

        try:
            # 'deposit_product' 필드에 ID만 보내는 대신 전체 정보를 직렬화하여 저장
            user_deposit = UserDeposit.objects.create(
                user=request.user,
                deposit_product=deposit_product,
                amount=amount
            )

            # 다시 UserDepositSerializer를 사용하여 응답
            user_deposit_serializer = UserDepositSerializer(user_deposit)
            return Response(user_deposit_serializer.data, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

# 예금 삭제 (DELETE)


class UserDepositDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            user_deposit = UserDeposit.objects.get(id=pk)
        except UserDeposit.DoesNotExist:
            return Response({"error": "Deposit not found"}, status=status.HTTP_404_NOT_FOUND)

        # 삭제할 예금이 현재 로그인한 사용자에 속하는지 확인
        if user_deposit.user != request.user:
            return Response({"error": "You cannot delete someone else's deposit"}, status=status.HTTP_403_FORBIDDEN)

        user_deposit.delete()
        return Response({"message": "Deposit deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def save_products(request):
    api_key = settings.DEPOSIT_API_KEY
    # 금융회사가 속한 권역 코드 Ex) 020000(은행), 030200(여신전문), 030300(저축은행), 050000(보험), 060000(금융투자)
    topFinGrpNo = '020000'
    pageNo = '1'  # 조회하고자 하는 페이지 번호 Ex) 1, 2, 3
    financeCd = ''  # 금융회사 코드 또는 명 Ex) 0010587, 0010588, 0010722, 국민, 상호, 하나

    deposit_url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
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
        max_limit = li.get('max_limit') or '없음'  # 최고한도
        dcls_strt_day = li.get('dcls_strt_day')  # 공시 시작일
        dcls_end_day = li.get('dcls_end_day') or '없음'  # 공시 종료일
        fin_co_subm_day = li.get('fin_co_subm_day')  # 금융회사 제출일

        if DepositProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            continue

        save_data = {
            'fin_prdt_cd': fin_prdt_cd,
            'kor_co_nm': kor_co_nm,
            'dcls_month': dcls_month,
            'fin_co_no': fin_co_no,
            'mtrt_int': mtrt_int,
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
            'dcls_month': dcls_month,
            'fin_co_no': fin_co_no,
            'mtrt_int': mtrt_int,
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
        product, created = DepositProduct.objects.get_or_create(
            fin_prdt_cd=fin_prdt_cd)
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
            'intr_rate_type': intr_rate_type,
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
        product, created = SavingProduct.objects.get_or_create(
            fin_prdt_cd=fin_prdt_cd)
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
            'intr_rate_type': intr_rate_type,
            'intr_rate_type_nm': intr_rate_type_nm,
            'intr_rate': intr_rate,
            'intr_rate2': intr_rate2,
            'save_trm': save_trm,
            'rsrv_type': rsrv_type,
            'rsrv_type_nm': rsrv_type_nm
        }

        serializer = SavingOptionsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    return JsonResponse({'message': '저장 성공!'})

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
        'deposit_product': product_serializer.data,
        'option': option_serializer.data,
    })
