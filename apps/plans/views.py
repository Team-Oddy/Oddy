import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import UserProfile, TravelGroup
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings
from django.contrib.auth import logout as django_logout
from allauth.socialaccount.models import SocialToken
from django.views.decorators.http import require_http_methods
import random
import string
import re
from .forms import TravelGroupForm
from .models import TravelGroup, TravelPlan
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from .models import TravelGroup, TravelPlan


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
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        data = json.loads(request.body)
        nickname = data.get('nickname')
        if nickname and len(nickname) <= 5:
            user_profile.nickname = nickname
            user_profile.save()
            return JsonResponse({'success': True, 'message': '닉네임 저장 완료'})
        else:
            return JsonResponse({'success': False, 'error': '닉네임은 5글자 이내로 작성해주세요.'})
    
    # GET 요청 처리
    has_nickname = bool(user_profile.nickname)
    has_travel_group = TravelGroup.objects.filter(creator=user_profile).exists()
    has_travel_type = bool(user_profile.travel_type)

    context = {
        'has_nickname': has_nickname,
        'has_travel_group': has_travel_group,
        'has_travel_type': has_travel_type,
    }

    return render(request, 'create_group.html', context)

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
                    creator=user_profile,  # creator 필드 설정
                    travel_name=travel_name,
                    start_date=start_date,
                    end_date=end_date,
                )
                travel_group.save()
                travel_group.members.add(user_profile)  # members ManyToMany 필드에 사용자 프로필 추가
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
    travel_group = get_object_or_404(TravelGroup, id=travel_group_id, creator=request.user.userprofile)
    travel_group.delete()
    return JsonResponse({'success': True, 'message': '여행 모임이 삭제되었습니다.'})

def complete_page(request):
    return render(request, 'create_group.html', {'completed': True})

def test(request):
    return render(request, 'test.html')

@login_required
def my_page(request):
    user_profile = request.user.userprofile
    travel_groups = user_profile.joined_travel_groups.all()
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


#여행유형 저장(선아)
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
from .models import UserProfile
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
                if travel_group.members.filter(id=user_profile.id).exists():
                    form.add_error('invite_code', 'You are already in this group.')
                else:
                    travel_group.members.add(user_profile)
                    travel_group.save()
                    return redirect('plans:my_page')
            except TravelGroup.DoesNotExist:
                form.add_error('invite_code', 'Invalid invite code.')
    else:
        form = InviteCodeForm()
    
    return render(request, 'join_group.html', {'form': form})




@login_required
def create_travel(request):
    if request.method == 'POST':
        form = TravelGroupForm(request.POST)
        if form.is_valid():
            travel_group = form.save(commit=False)
            travel_group.creator = request.user.userprofile
            travel_group.save()
            travel_group.members.add(request.user.userprofile)
            return redirect('plans:timetable', travel_group_id=travel_group.id)
    else:
        form = TravelGroupForm()

    latest_travel_group = TravelGroup.objects.order_by('-id').first()
    
    if latest_travel_group:
        travel_name = latest_travel_group.travel_name
        start_date = latest_travel_group.start_date
        end_date = latest_travel_group.end_date

        # 현재 날짜를 기준으로 D-Day 계산
        today = datetime.today().date()
        d_day = (start_date - today).days
    else:
        travel_name = '여행 이름 없음'
        d_day = None

    context = {
        'form': form,
        'travel_name': travel_name,
        'd_day': d_day,
        'travel_group': latest_travel_group
    }

    return render(request, 'create_travel.html', context)

def travel_map(request):
    return render(request, 'travel_map.html')



#map예제 추가해봤으나 검색은 안되는 중.. 지도는 잘 불러와짐
from django.shortcuts import render

def map_view(request):
    return render(request, 'map.html')


##의진// 새로운 여행 계획(4가지카테고리)추가[add_travel_plan], 특정 여행 그룹 필터링[get_travel_plans], 특정 여행 계획 삭제[delete_travel_plan], 특정 여행 그룹의 상세 계획[trave_plans]
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import TravelGroup, TravelPlan
import json

@login_required
@require_POST
def add_travel_plan(request, group_id):
    travel_group = get_object_or_404(TravelGroup, id=group_id)
    if request.user.userprofile not in travel_group.members.all():
        return JsonResponse({'status': 'error', 'message': 'Permission denied'})
    
    data = json.loads(request.body)
    category = data.get('category')
    place = data.get('place')
    address = data.get('address')
    description = data.get('description')
    
    if not all([category, place,address, description]):
        return JsonResponse({'status': 'error', 'message': 'Missing required fields'})
    
    plan = TravelPlan.objects.create(
        travel_group=travel_group,
        creator=request.user.userprofile,
        category=category,
        place=place,
        address=address,
        description=description
    )
    
    return JsonResponse({
        'status': 'success',
        'id': plan.id,
        'category': plan.category,
        'place': plan.place,
        'address': plan.address,
        'description': plan.description,
        'creator': plan.creator.nickname or plan.creator.user.username
    })

@login_required
def get_travel_plans(request, group_id):
    travel_group = get_object_or_404(TravelGroup, id=group_id)
    if request.user.userprofile not in travel_group.members.all():
        return JsonResponse({'status': 'error', 'message': 'Permission denied'})
    
    category = request.GET.get('category')
    if category:
        plans = TravelPlan.objects.filter(travel_group=travel_group, category=category).order_by('-created_at')
    else:
        plans = TravelPlan.objects.filter(travel_group=travel_group).order_by('category', '-created_at')
    

    plans_data = [{
        'id': plan.id,
        'category': plan.category,
        'place': plan.place,
        'description': plan.description,
        'creator': plan.creator.nickname or plan.creator.user.username,
        'created_at': plan.created_at.isoformat(),
    } for plan in plans]
    
    return JsonResponse({'status': 'success', 'plans': plans_data})

@login_required
@require_POST
def delete_travel_plan(request, plan_id):
    plan = get_object_or_404(TravelPlan, id=plan_id)
    if request.user.userprofile != plan.creator and request.user.userprofile != plan.travel_group.creator:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'})
    
    plan.delete()
    return JsonResponse({'status': 'success', 'message': 'Plan deleted successfully'})

@login_required
def travel_plan_detail(request, group_id):
    travel_group = get_object_or_404(TravelGroup, id=group_id)
    if request.user.userprofile not in travel_group.members.all():
        return JsonResponse({'status': 'error', 'message': 'Permission denied'})
    
    plans = TravelPlan.objects.filter(travel_group=travel_group).order_by('category', '-created_at')
    context = {
        'travel_group': travel_group,
        'plans': plans,
    }
    return render(request, 'travel_plan_detail.html', context)



def search_view(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        results = []
        if query:
            url = "https://openapi.naver.com/v1/search/local.json"
            headers = {
                "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
                "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET
            }
            params = {
                "query": query,
                "display": 10,
                "start": 1,
                "sort": "random"
            }
            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()  # Raises an HTTPError for bad responses
                data = response.json()
                results = data.get('items', [])
                
                for item in results:
                    item['title'] = re.sub('<[^<]+?>', '', item['title'])
                    # Convert coordinates to float if they exist
                    if 'mapx' in item:
                        item['mapx'] = float(item['mapx'])
                    if 'mapy' in item:
                        item['mapy'] = float(item['mapy'])
                
            except requests.RequestException as e:
                print(f"API request failed: {e}")
                results = []
        
        context = {
            'results': results,
            'query': query,
            'ncp_client_id': settings.NAVER_CLIENT_ID
        }
        return JsonResponse({'results': results, 'query': query})
    

#시간표 부분
from django.core.paginator import Paginator

def timetable_view(request, travel_group_id):
    travel_group = get_object_or_404(TravelGroup, id=travel_group_id)
    travel_plans = TravelPlan.objects.filter(travel_group=travel_group)

    # 날짜 범위 생성
    date_range = [travel_group.start_date + timedelta(days=x) for x in range((travel_group.end_date - travel_group.start_date).days + 1)]

    # 페이지네이터를 사용하여 날짜를 4일씩 페이지네이션
    paginator = Paginator(date_range, 4)  # 4일씩 페이지네이션
    page_number = request.GET.get('page')  # URL에서 페이지 번호를 가져옴
    page_obj = paginator.get_page(page_number)

    hours = range(9, 22)
    context = {
        'travel_group': travel_group,
        'travel_plans': travel_plans,
        'date_range': page_obj.object_list,
        'hours': hours,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page_url': f"?page={page_obj.previous_page_number()}" if page_obj.has_previous() else None,
        'next_page_url': f"?page={page_obj.next_page_number()}" if page_obj.has_next() else None,
        'available_dates': date_range,
    }
    return render(request, 'timetable.html', context)

@require_POST
def add_timetable_plan(request, travel_group_id):
    travel_group = get_object_or_404(TravelGroup, id=travel_group_id)
    data = json.loads(request.body)

    date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    time = datetime.strptime(data['time'], '%H:%M').time()

    new_plan = TravelPlan.objects.create(
        travel_group=travel_group,
        creator=request.user.userprofile,
        category=data['category'],
        place=data['place'],
        description=data['description'],
        date=date,
        time=time
    )

    return JsonResponse({
        'status': 'success', 
        'plan_id': new_plan.id,
        'category': new_plan.category,
        'place': new_plan.place,
        'date': new_plan.date.strftime('%Y-%m-%d'),
        'time': new_plan.time.strftime('%H:%M')
    })

def get_all_plans(request, travel_group_id):
    travel_group = get_object_or_404(TravelGroup, id=travel_group_id)
    plans = TravelPlan.objects.filter(travel_group=travel_group)
    plans_data = [{
        'id': plan.id,
        'category': plan.category,
        'place': plan.place,
        'description': plan.description,
        'date': plan.date.strftime('%Y-%m-%d') if plan.date else None,
        'plan_start_time': plan.plan_start_time.strftime('%H:%M') if plan.plan_start_time else None,
        'plan_end_time': plan.plan_end_time.strftime('%H:%M') if plan.plan_end_time else None
    } for plan in plans]
    return JsonResponse(plans_data, safe=False)

def get_plans(request, travel_group_id):
    travel_group = get_object_or_404(TravelGroup, id=travel_group_id)
    category = request.GET.get('category')
    if category:
        plans = TravelPlan.objects.filter(travel_group=travel_group, category=category)
    else:
        plans = TravelPlan.objects.filter(travel_group=travel_group)
    
    plans_data = [{
        'id': plan.id,
        'category': plan.category,
        'place': plan.place,
        'description': plan.description,
        'date': plan.date.strftime('%Y-%m-%d') if plan.date else None,
        'plan_start_time': plan.plan_start_time.strftime('%H:%M') if plan.plan_start_time else None,
        'plan_end_time': plan.plan_end_time.strftime('%H:%M') if plan.plan_end_time else None
    } for plan in plans]
    return JsonResponse(plans_data, safe=False)

import json
import re
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import TravelPlan
@require_POST
def update_plan_datetime(request):
    try:
        data = json.loads(request.body)
        plan_id = data.get('plan_id')
        date_str = data.get('date')
        plan_start_time = data.get('plan_start_time')
        plan_end_time = data.get('plan_end_time')

        plan = get_object_or_404(TravelPlan, id=plan_id)

        # 이전 계획 정보 저장
        old_plan = {
            'id': plan.id,
            'date': plan.date,
            'plan_start_time': plan.plan_start_time,
            'plan_end_time': plan.plan_end_time,
            'category': plan.category,
            'place': plan.place
        }

        # 날짜가 None이 아닌 경우에만 변환 작업 수행
        if date_str:
            date_str = re.sub(r'(\d{4})년\s(\d{1,2})월\s(\d{1,2})일', r'\1-\2-\3', date_str)
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            plan.date = date
        else:
            # 날짜가 null일 경우, None으로 설정
            plan.date = None

        # 시작 및 종료 시간이 제공되었는지 확인
        plan.plan_start_time = plan_start_time if plan_start_time else None
        plan.plan_end_time = plan_end_time if plan_end_time else None

        plan.save()

        # 새로운 계획 정보
        new_plan = {
            'id': plan.id,
            'date': plan.date,
            'plan_start_time': plan.plan_start_time,
            'plan_end_time': plan.plan_end_time,
            'category': plan.category,
            'place': plan.place
        }

        return JsonResponse({
            'status': 'success',
            'category': plan.category,
            'old_plan': old_plan,
            'new_plan': new_plan
        })

    except TravelPlan.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Plan not found'}, status=404)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


#좋아요
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import TravelPlan, Like, Comment
from django.contrib.auth.decorators import login_required

@login_required
def toggle_like(request, id):
    user = request.user.userprofile
    travel_plan = get_object_or_404(TravelPlan, id=id)

    # 좋아요가 이미 있는지 확인
    existing_like = Like.objects.filter(travel_plan=travel_plan, user=user).first()

    if existing_like:
        # 이미 좋아요가 있는 경우 삭제
        existing_like.delete()
        liked = False
    else:
        # 좋아요가 없는 경우 추가
        Like.objects.create(travel_plan=travel_plan, user=user)
        liked = True

    # 좋아요 수 업데이트
    travel_plan.like_count = travel_plan.likes.count()
    travel_plan.save()

    return JsonResponse({
        'liked': liked,
        'like_count': travel_plan.like_count
    })


    
@login_required
@require_POST
def add_comment(request, plan_id):
    user_profile = request.user.userprofile
    travel_plan = TravelPlan.objects.get(id=plan_id)
    content = request.POST.get('content')

    if content:
        # 댓글 생성
        comment = Comment.objects.create(user=user_profile, travel_plan=travel_plan, content=content)
        comment_count = travel_plan.comments.count()

        # 새로 생성된 댓글 데이터를 반환
        comment_data = {
            'id': comment.id,
            'user': comment.user.nickname,  # 댓글 작성자의 닉네임
            'content': comment.content,
            'created_at': comment.created_at.isoformat()
        }

        return JsonResponse({'success': True, 'comment_count': comment_count, 'comment': comment_data})
    else:
        return JsonResponse({'success': False, 'error': '댓글 내용을 입력해주세요.'})

@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)

    if request.user.userprofile == comment.user:
        comment.delete()
        comment_count = comment.travel_plan.comments.count()
        return JsonResponse({'success': True, 'comment_count': comment_count, 'comment_id': comment_id})
    else:
        return JsonResponse({'success': False, 'error': '삭제할 권한이 없습니다.'})

def get_comments(request, plan_id):
    travel_plan = get_object_or_404(TravelPlan, id=plan_id)
    comments = Comment.objects.filter(travel_plan=travel_plan).order_by('created_at')

    comments_data = [{
        'id': comment.id,
        'user': comment.user.nickname,
        'content': comment.content,
        'created_at': comment.created_at.isoformat()
    } for comment in comments]

    return JsonResponse({'success': True, 'comments': comments_data})


#지도 마커 구현 코드
def travel_map(request, travel_group_id):
    travel_group = get_object_or_404(TravelGroup, id=travel_group_id)
    travel_plans = TravelPlan.objects.filter(travel_group=travel_group)
    
    context = {
        'travel_group': travel_group,
        'travel_plans': travel_plans,
    }
    return render(request, 'travel_map.html', context)


from django.shortcuts import render

def create_group_like(request):
    return render(request, 'create_group.html', {
        'scroll_to_options': True  # optionsPage로 이동하기 위한 플래그
    })


@require_POST
def save_airplane_text(request):
    try:
        data = json.loads(request.body)
        plan_id = data.get('plan_id')
        airplane_text = data.get('airplane_text')

        plan = get_object_or_404(TravelPlan, id=plan_id)
        # 여기에 airplane_text를 저장할 필드가 있다고 가정합니다.
        plan.airplane_text = airplane_text
        plan.save()

        return JsonResponse({'status': 'success'})
    
    except TravelPlan.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Plan not found'}, status=404)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)