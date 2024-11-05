import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# API 키와 서비스 계정 키 파일 경로 설정
SERVICE_ACCOUNT_FILE = 'path/to/your/service-account-file.json'  # 서비스 계정 JSON 파일 경로
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

# 인증 및 서비스 객체 생성
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('webmasters', 'v3', credentials=credentials)

# Search Console 사이트 URL 설정
site_url = 'https://www.yoursite.com/'  # 여러분의 사이트 URL로 변경하세요

# 데이터 요청
response = service.searchanalytics().query(
    siteUrl=site_url,
    body={
        'startDate': '2024-01-01',
        'endDate': '2024-01-31',
        'dimensions': ['query', 'page'],
        'rowLimit': 10
    }
).execute()

# 결과 출력
print(json.dumps(response, indent=2, ensure_ascii=False))
