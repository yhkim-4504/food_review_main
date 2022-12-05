from django.shortcuts import render
from django.http import HttpResponse
from .serializers import ReviewSerializer
from main.models import Review

# Create your views here.
def test(request):
    return HttpResponse('analysis:test')
