from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.conf import settings
import time

# def index(request):
#     api_key = settings.EXCHANGE_API_KEY  # API 키 설정

#     url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
#     params = {
#         "authkey": api_key,
#         "data": "AP01",
#     }

#     max_retries = 3
#     timeout = 5  # 5초 타임아웃 설정

#     for attempt in range(max_retries):
#         try:
#             response = requests.get(url, params=params, timeout=timeout)
#             response.raise_for_status()
#             rates = response.json()
#             return render(request, 'exchanges/index.html', {'rates': rates})
#         except requests.exceptions.RequestException as e:
#             if attempt < max_retries - 1:
#                 time.sleep(2)  # 2초 대기 후 재시도
#                 continue
#             return render(request, 'exchanges/index.html', {'error': str(e)})


def index(request):
    api_key = settings.EXCHANGE_API_KEY  # API 키 설정

    url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
    params = {
        "authkey": api_key,
        "data": "AP01",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        rates = response.json()
        return JsonResponse({'rates': rates})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
        
def bankmap(request):
    return render(request, 'exchanges/bankmap.html')

def test(request):
    return render(request, 'exchanges/test.html')