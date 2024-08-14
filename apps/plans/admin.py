from django.contrib import admin
from .models import UserProfile, TravelGroup, TravelPlan, Like, Comment

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'travel_type')
    search_fields = ('user__username', 'nickname')

@admin.register(TravelGroup)
class TravelGroupAdmin(admin.ModelAdmin):
    list_display = ('travel_name', 'creator', 'start_date', 'end_date', 'invite_code')
    search_fields = ('travel_name', 'creator__nickname')
    filter_horizontal = ('members',)

@admin.register(TravelPlan)
class TravelPlanAdmin(admin.ModelAdmin):
    list_display = ('travel_group', 'creator', 'category', 'place', 'date', 'plan_start_time', 'plan_end_time', 'like_count', 'comment_count')
    list_filter = ('category', 'date')
    search_fields = ('place', 'description')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'travel_plan', 'created_at')
    list_filter = ('created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'travel_plan', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)