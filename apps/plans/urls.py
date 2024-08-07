from django.urls import path
from .views import *

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
    
    #초대코드를 입력하는 페이지
    path('join_group_page/', join_group_page, name='join_group_page'),
    #map view
    path('map/', map_view, name='map_view'),
]