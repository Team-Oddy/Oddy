from django.contrib import admin
from .models import UserProfile, TravelGroup

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
        return ", ".join([profile.nickname for profile in obj.user_profiles.all()])
    get_user_profiles.short_description = 'User Profiles'

admin.site.register(TravelGroup, TravelGroupAdmin)
