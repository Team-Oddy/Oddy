import os
from django.core.management.utils import get_random_secret_key
from django.contrib.auth.models import User
from django.core.management import execute_from_command_line

# 환경 변수에서 superuser 정보 가져오기
DJANGO_SUPERUSER_USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME')
DJANGO_SUPERUSER_EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL')
DJANGO_SUPERUSER_PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

# 데이터베이스 초기화
execute_from_command_line(['manage.py', 'flush', '--no-input'])

# 마이그레이션 적용
execute_from_command_line(['manage.py', 'migrate'])

# Superuser 생성
if not User.objects.filter(username=DJANGO_SUPERUSER_USERNAME).exists():
    User.objects.create_superuser(DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD)
    print(f"Superuser {DJANGO_SUPERUSER_USERNAME} created successfully")
else:
    print(f"Superuser {DJANGO_SUPERUSER_USERNAME} already exists")
