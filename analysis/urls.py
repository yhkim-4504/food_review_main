from django.urls import path
from . import views

app_name = 'analysis'

urlpatterns = [
    path('', views.review_analysis, name='review_analysis'),
]
