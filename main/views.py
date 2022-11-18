from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .forms import ReviewForm

# Create your views here.
def main_page(request):
    return render(request, 'main/main.html')

def menu_page(request):
    return render(request, 'main/menu.html')

def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            review = form.save(commit=False)
            review.image = request.FILES.get('image')
            review.create_date = timezone.now()
            review.save()

        return render(request, 'main/review_create.html')
    else:
        form = ReviewForm()
        context = {
            'form': form
        }

        return render(request, 'main/review_create.html', context)