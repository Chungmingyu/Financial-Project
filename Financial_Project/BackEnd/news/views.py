import requests
from django.http import JsonResponse
from django.conf import settings

def fetch_google_news(request):
    query = request.GET.get('q', 'latest news')  # 검색어 (예: 'latest news')
    api_key = settings.GOOGLE_API_KEY  # settings.py에 저장된 API 키
    cse_id = settings.GOOGLE_CSE_ID  # Custom Search Engine ID
    
    # API 호출 URL
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cse_id}"
    response = requests.get(url)
    data = response.json()

    
    # 필요한 정보만 추출 (예: 제목과 링크)
    news_items = data.get("items", [])
    
    return JsonResponse({"news": news_items})

