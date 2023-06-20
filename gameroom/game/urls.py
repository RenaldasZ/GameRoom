from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hiscore/', views.HiScoreListView.as_view(), name='hiscore'),
    path('player/', views.PlayerList.as_view()),
]
