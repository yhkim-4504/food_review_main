import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .serializers import ReviewSerializer
from main.models import Review
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import AnalysisForm

# Create your views here.
@login_required(login_url='common:login')
@api_view(['GET', 'POST'])
def review_analysis(request):
    if request.method == 'POST':
        form = AnalysisForm(request.POST)
        print(request.POST.get('startdate'))
        #return Response({''})
        return render(request, 'analysis/review_analysis.html', {'form': form})
    else:
        form = AnalysisForm()
        return render(request, 'analysis/review_analysis.html', {'form': form})
