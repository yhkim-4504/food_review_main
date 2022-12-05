import datetime
from django.shortcuts import render
from django.http import HttpResponse
from main.models import Review
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .forms import AnalysisForm
from .serializers import ReviewSerializer

# Create your views here.
@login_required(login_url='common:login')
@api_view(['GET', 'POST'])
def review_analysis(request):
    if request.method == 'POST':
        form = AnalysisForm(request.POST)
        
        if form.is_valid():
            # Set range
            start_date, end_date = request.POST.get('startdate'), request.POST.get('enddate')
            start_datetime = datetime.datetime.combine(datetime.datetime.strptime(start_date, '%Y-%m-%d'), datetime.time.min)
            end_datetime = datetime.datetime.combine(datetime.datetime.strptime(end_date, '%Y-%m-%d'), datetime.time.max)
            
            # Query range objects
            review_range_objects = Review.objects.filter(create_date__range=(timezone.make_aware(start_datetime), timezone.make_aware(end_datetime)))

            return Response(ReviewSerializer(review_range_objects, many=True).data)
    else:
        form = AnalysisForm()

    return render(request, 'analysis/review_analysis.html', {'form': form})
