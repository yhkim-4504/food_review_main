from django.urls import path
from . import views

app_name = 'analysis'

urlpatterns = [
    path('test/', views.test, name='test'),
]
