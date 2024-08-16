from django.urls import path
from .views import *
from . import views

app_name='plans'

urlpatterns=[
    path('', main, name='main'),
    path('create_group/', create_group, name='create_group'),
    path('travel_name_page/', travel_name_page, name='travel_name_page'),
    path('complete/', complete_page, name='complete_page'),
    path('test/', test, name='test'),
    path('my_page/', my_page, name='my_page'),
    path('update_nickname/', update_nickname, name='update_nickname'),
    path('logout/', kakao_logout, name='kakao_logout'),
    path('save_test_result/', save_test_result, name='save_test_result'),
    path('create_travel/', create_travel, name='create_travel'),
    path('travel_map/', travel_map, name='travel_map'),
    path('timetable/<int:travel_group_id>/', views.timetable_view, name='timetable'),
    path('add_timetable_plan/<int:travel_group_id>/', views.add_timetable_plan, name='add_timetable_plan'),
    path('get_all_plans/<int:travel_group_id>/', views.get_all_plans, name='get_all_plans'),
    path('get_plans/<int:travel_group_id>/', views.get_plans, name='get_plans'),
    #초대코드를 입력하는 페이지
    path('join_group_page/', join_group_page, name='join_group_page'),
    path('group/<int:group_id>/', views.create_travel, name='create_travel_with_id'),
    #map view
    path('travel_map/<int:travel_group_id>/', views.travel_map, name='travel_map'),
    path('travel_map/', views.travel_map, name='travel_map'),
    path('travel_map/<int:travel_group_id>/', views.travel_map, name='travel_map_with_id'),
    #travel plans
    path('group/<int:group_id>/add_plan/', add_travel_plan, name='add_travel_plan'),
    path('group/<int:group_id>/get_plans/', get_travel_plans, name='get_travel_plans'),
    path('plans/plan/<int:plan_id>/delete/', delete_travel_plan, name='delete_travel_plan'),
    path('plan/<int:plan_id>/detail/', travel_plan_detail, name='travel_plan_detail'),
    path('search/', search_view, name='search'),
    path('timetable/<int:travel_group_id>/', views.timetable_view, name='timetable'),
    path('add_timetable_plan/<int:travel_group_id>/', views.add_timetable_plan, name='add_timetable_plan'),
    path('update_plan_datetime/', views.update_plan_datetime, name='update_plan_datetime'),

    path('like/<int:id>/', toggle_like, name='toggle_like'),
    path('like/status/<int:id>/', get_like_status, name='get_like_status'),
    path('plans/<int:plan_id>/comments/', get_comments, name='get_comments'),
    path('comment/add/<int:plan_id>/', add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    
    path('save_airplane_text/', views.save_airplane_text, name='save_airplane_text'),
    
    path('kakao/', kakao_view, name='kakao_link'),
    
    
    path('get_kakao_share_data/<int:travel_group_id>/', views.get_kakao_share_data, name='get_kakao_share_data'),
]