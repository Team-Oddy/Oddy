from django.urls import path
from .views import *

app_name='plans'

urlpatterns=[
    path('', main, name='main'),
    path('create_group/', create_group, name='create_group'),
    path('test/', test, name='test'),
]