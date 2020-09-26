from django.urls import path
from . import views
urlpatterns = [
    path('index/', views.index, name='index'),
    path('list/', views.list, name='list'),
    path('map/', views.map, name='map'),
    path('mapsearch/', views.mapsearch, name='mapsearch'),
    path('resinfo/', views.resinfo, name='resinfo'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name="register"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('review/write/', views.review_write, name="review_write"),
    path('review/delete/', views.review_delete, name="review_delete"),
    path('bbs/', views.bbslistview, name="bbs"),
    path('bbswrite/', views.bbswrite, name="bbswrite"),
    path('bbsdetail/', views.bbsdetail, name="bbsdetail"),
    path('bbsupdate/', views.bbsupdate, name="bbsupdate"),
    path('bbsdelete/', views.bbsdelete, name="bbsdelete"),
]