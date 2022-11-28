from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.main_page, name='main'),
    path('menu/', views.menu_page, name='menu'),
    path('review/create/', views.review_create, name='review_create'),
    path('review/', views.review_display, name='review_display'),
]
