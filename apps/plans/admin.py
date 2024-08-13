from django.contrib import admin
from .models import UserProfile, TravelGroup, TravelPlan, Like, Comment

# UserProfile 모델을 admin 사이트에 등록
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'travel_type')  # 관리 화면에 표시할 필드
    search_fields = ('nickname',)  # 검색 가능한 필드

admin.site.register(UserProfile, UserProfileAdmin)

# TravelGroup 모델을 admin 사이트에 등록
class TravelGroupAdmin(admin.ModelAdmin):
    list_display = ('travel_name', 'start_date', 'end_date', 'invite_code', 'get_user_profiles')  # 관리 화면에 표시할 필드
    search_fields = ('travel_name', 'invite_code')  # 검색 가능한 필드

    def get_user_profiles(self, obj):
        return ", ".join([profile.nickname for profile in obj.members.all()])
    get_user_profiles.short_description = 'User Profiles'

admin.site.register(TravelGroup, TravelGroupAdmin)

# TravelPlan 모델을 admin 사이트에 등록
class TravelPlanAdmin(admin.ModelAdmin):
    list_display = ('travel_group', 'creator', 'category', 'place', 'address', 'date', 'plan_start_time', 'plan_end_time', 'like_count', 'comment_count', 'created_at', 'updated_at')  # 관리 화면에 표시할 필드
    search_fields = ('place', 'description')  # 검색 가능한 필드
    list_filter = ('category', 'date')  # 필터 옵션 추가
    date_hierarchy = 'date'  # 날짜 계층화 추가

admin.site.register(TravelPlan, TravelPlanAdmin)

# Like 모델을 admin 사이트에 등록
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'travel_plan', 'created_at')  # 관리 화면에 표시할 필드
    search_fields = ('user__nickname', 'travel_plan__place')  # 검색 가능한 필드
    list_filter = ('created_at',)  # 필터 옵션 추가
    date_hierarchy = 'created_at'  # 날짜 계층화 추가

admin.site.register(Like, LikeAdmin)

# Comment 모델을 admin 사이트에 등록
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'travel_plan', 'content', 'created_at')  # 관리 화면에 표시할 필드
    search_fields = ('user__nickname', 'travel_plan__place', 'content')  # 검색 가능한 필드
    list_filter = ('created_at',)  # 필터 옵션 추가
    date_hierarchy = 'created_at'  # 날짜 계층화 추가

admin.site.register(Comment, CommentAdmin)
