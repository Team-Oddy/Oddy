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
from allauth.socialaccount.models import SocialToken
from django.views.decorators.http import require_http_methods

import random
import string

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



@login_required
@require_http_methods(["GET", "POST"])
def set_nickname(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nickname = data.get('nickname')
        if nickname and len(nickname) <= 5:
            user_profile, created = UserProfile.objects.update_or_create(
                user=request.user,
                defaults={'nickname': nickname}
            )
            return JsonResponse({'success': True, 'message': '닉네임 저장 완료'})
        else:
            return JsonResponse({'success': False, 'error': '닉네임은 5글자 이내로 작성해주세요.'})
    else:
        try:
            current_nickname = request.user.userprofile.nickname
        except UserProfile.DoesNotExist:
            current_nickname = ""
        return JsonResponse({'nickname': current_nickname})

@login_required
@require_http_methods(["GET", "POST"])
def create_group(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nickname = data.get('nickname')
        if nickname and len(nickname) <= 5:
            user = request.user
            user_profile, created = UserProfile.objects.update_or_create(
                user=user,
                defaults={'nickname': nickname}
            )
            return JsonResponse({'success': True, 'message': '닉네임 저장 완료'})
        else:
            return JsonResponse({'success': False, 'error': '닉네임은 5글자 이내로 작성해주세요.'})
    return render(request, 'create_group.html')

@csrf_exempt
@login_required
def travel_name_page(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        travel_name = data.get('travelName')
        start_date = data.get('travelStartDate')
        end_date = data.get('travelEndDate')
        
        if len(travel_name) <= 15 and start_date and end_date:
            try:
                user_profile = request.user.userprofile
                travel_group = TravelGroup(
                    travel_name=travel_name,
                    start_date=start_date,
                    end_date=end_date,
                )
                travel_group.save()
                travel_group.user_profiles.add(user_profile)  # Many-to-Many 필드에 사용자 프로필 추가
                return JsonResponse({'success': True, 'message': '여행 모임 저장 완료'})
            except UserProfile.DoesNotExist:
                return JsonResponse({'success': False, 'error': '사용자 프로필이 존재하지 않습니다.'})
        else:
            return JsonResponse({'success': False, 'error': '여행 이름은 15글자 이내로 작성해야 하며, 모든 날짜를 입력해야 합니다.'})
    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})


def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))



@login_required
@require_http_methods(["POST"])
def delete_travel_group(request, travel_group_id):
    travel_group = get_object_or_404(TravelGroup, id=travel_group_id, user_profile=request.user.userprofile)
    travel_group.delete()
    return JsonResponse({'success': True, 'message': '여행 모임이 삭제되었습니다.'})

def complete_page(request):
    return render(request, 'create_group.html', {'completed': True})

def test(request):
    return render(request, 'test.html')

@login_required
def my_page(request):
    user_profile = request.user.userprofile
    travel_groups = user_profile.travel_groups.all()
    return render(request, 'my_page.html', {'user_profile': user_profile, 'travel_groups': travel_groups})


@login_required 
@csrf_exempt
def update_nickname(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_nickname = data.get('nickname')
        if new_nickname and len(new_nickname) <= 5:
            try:
                user_profile = UserProfile.objects.get(user=request.user) 
            except UserProfile.DoesNotExist:
                return JsonResponse({'success': False, 'error': '사용자 프로필이 존재하지 않습니다.'})
            user_profile.nickname = new_nickname  
            user_profile.save()
            return JsonResponse({'success': True, 'message': '닉네임이 성공적으로 변경되었습니다.'})
        else:
            return JsonResponse({'success': False, 'error': '닉네임은 5글자 이내로 작성해주세요.'})
    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})

@login_required
@csrf_exempt
def save_test_result(request): 
    if request.method == 'POST':
        data = json.loads(request.body)
        answers = data.get('answers')
        user = request.user
        nickname = get_object_or_404(UserProfile, user=request.user).nickname
        travel_type = determine_travel_type(answers)
        try:
            user_profile = UserProfile.objects.get(id=user.id)
            user_profile.travel_type = travel_type
            user_profile.save()
            return JsonResponse({'success': True, 'travel_type': travel_type, 'nickname': nickname})
        except UserProfile.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'UserProfile matching query does not exist.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def determine_travel_type(answers):
    first_letters = [answer[0] for answer in answers]
    count_a = first_letters.count('a')
    count_b = first_letters.count('b')
    count_c = first_letters.count('c')
    print(count_a, count_b, count_c)

    if count_a >= 3:
        return '완벽주의 플래너형'
    elif count_b >= 3:
        return '자유로운 모험가형'
    elif count_c >= 3:
        if (
            (answers[1].startswith('c') and answers[4].startswith('c')) or
            (answers[1].startswith('c') and answers[2].startswith('c') and answers[3].startswith('c')) or
            (answers[1].startswith('c') and answers[2].startswith('c') and answers[3].startswith('c') and answers[4].startswith('c')) or
            (answers[1].startswith('c') and answers[3].startswith('c') and answers[4].startswith('c'))
        ):
            return '휴식 추구형'
        elif answers[1].startswith('c'):
            return '미식 탐험가형'
        else:
            return '미식 탐험가형'
    else:
        return '균형 잡힌 탐험가형'
    
#초대코드 처리로직
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import InviteCodeForm
from .models import TravelGroup

@login_required
def join_group_page(request):
    if request.method == 'POST':
        form = InviteCodeForm(request.POST)
        if form.is_valid():
            invite_code = form.cleaned_data['invite_code']
            try:
                travel_group = TravelGroup.objects.get(invite_code=invite_code)
                user_profile = request.user.userprofile
                if travel_group.user_profiles.filter(id=user_profile.id).exists():
                    form.add_error('invite_code', 'You are already in this group.')
                else:
                    travel_group.user_profiles.add(user_profile)
                    travel_group.save()
                    return redirect('plans:my_page')
            except TravelGroup.DoesNotExist:
                form.add_error('invite_code', 'Invalid invite code.')
    else:
        form = InviteCodeForm()
    
    return render(request, 'join_group.html', {'form': form})
