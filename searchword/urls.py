from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
from django.contrib import admin  
from  searchword.views import GetTamilWord, GetGranthaWord, download



urlpatterns=[
    path('',views.home),
    path('tamil_words',GetTamilWord.as_view(), name='wordgame'),
    path('grantha_words',GetGranthaWord.as_view(), name='wordgame1'),
    path('download', views.download, name='download')
]


