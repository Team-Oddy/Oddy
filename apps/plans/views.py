import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import UserProfile, TravelGroup
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required

import requests
from django.conf import settings
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect
from allauth.socialaccount.models import SocialToken

#선아 작성 부분
def main(request):
    if request.user.is_authenticated:
        # 로그인된 사용자의 경우
        return render(request, 'main.html', {'plans': TravelGroup.objects.all()})
    else:
        # 비로그인 사용자의 경우
        return render(request, 'main.html')

@login_required
# 카카오톡 로그아웃
def kakao_logout(request):
    if request.user.is_authenticated:
        try:
            social_token = SocialToken.objects.get(account__user=request.user, account__provider='kakao')
            kakao_logout_url = 'https://kapi.kakao.com/v1/user/logout'
            headers = {
                'Authorization': f'Bearer {social_token.token}',
            }
            response = requests.post(kakao_logout_url, headers=headers)
            if response.status_code == 200:
                print('카카오 로그아웃 성공')
            else:
                print('카카오 로그아웃 실패', response.json())
        except SocialToken.DoesNotExist:
            print('카카오 소셜 토큰을 찾을 수 없습니다.')
        django_logout(request)

    return redirect('plans:main')





# Create your views here.

def create_group(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nickname = data.get('nickname')
        if nickname and len(nickname) <= 5:
            user_profile = UserProfile.objects.create(nickname=nickname)
            request.session['user_profile_id'] = user_profile.id
            return JsonResponse({'success': True, 'message': '닉네임 저장 완료'})
        else:
            return JsonResponse({'success': False, 'error': '닉네임은 5글자 이내로 작성해주세요.'})
    return render(request, 'create_group.html')

@csrf_exempt
def travel_name_page(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        travel_name = data.get('travelName')
        start_date = data.get('travelStartDate')
        end_date = data.get('travelEndDate')
        
        if len(travel_name) <= 15 and start_date and end_date:
            user_profile_id = request.session.get('user_profile_id')
            if user_profile_id:
                user_profile = UserProfile.objects.get(id=user_profile_id)
                travel_group = TravelGroup(
                    user_profile=user_profile,
                    travel_name=travel_name,
                    start_date=start_date,
                    end_date=end_date
                )
                travel_group.save()
                return JsonResponse({'success': True, 'message': '여행 모임 저장 완료'})
            else:
                return JsonResponse({'success': False, 'error': '사용자 프로필이 존재하지 않습니다.'})
        else:
            return JsonResponse({'success': False, 'error': '여행 이름은 15글자 이내로 작성해야 하며, 모든 날짜를 입력해야 합니다.'})
    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})

def complete_page(request):
    return render(request, 'create_group.html', {'completed': True})

def test(request):
    return render(request, 'test.html')

def my_page(request):
    return render(request, 'my_page.html')



