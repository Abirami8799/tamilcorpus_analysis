from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
from django.contrib import admin  
from  searchword.views import GetTamilWord



urlpatterns=[
    path('',views.home, name='home'),
    path('search/',GetTamilWord.as_view(), name='wordgame')
]


