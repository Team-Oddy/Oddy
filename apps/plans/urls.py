from django.urls import path
from .views import *

app_name='plans'

urlpatterns=[
    path('', main, name='main'),
    path('create_group/', create_group, name='create_group'),
    path('travel_name_page/', travel_name_page, name='travel_name_page'),
    path('complete/', complete_page, name='complete_page'),
    path('test/', test, name='test'),
    path('logout/', kakao_logout, name='kakao_logout'),
    path('save_test_result/', save_test_result, name='save_test_result'),
]