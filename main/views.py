import threading
from django import db
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import ReviewImage, Review
from .forms import ReviewForm
from grpc_ai_client.ai_client import GrpcClient
from django.contrib.auth.decorators import login_required

# Create your views here.
def main_page(request):
    return render(request, 'main/main.html')

def menu_page(request):
    return render(request, 'main/menu.html')

@csrf_exempt
@login_required(login_url='common:login')
def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.create_date = timezone.now()
            review.save()

            # POST 이미지 처리
            for i, image in enumerate(request.FILES.getlist('image')):
                image_bytes = image.read()
                review_image = ReviewImage(review_id=review, image=image, upload_date=timezone.now())
                review_image.save()

                if i == 0:
                    t = threading.Thread(target=inference_thread_func, args=(review, 'localhost', '50051', review.id, image_bytes))
                    t.start()
    else:
        form = ReviewForm()

    return render(request, 'main/review_create.html', {'form': form})
    
def review_display(request):
    objects = Review.objects.order_by('-create_date')
    per_page = 10

    # Paginator
    paginator = Paginator(objects, per_page=per_page)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)

    # Page indexes
    start_page = (page_obj.number//per_page) * 10 + 1
    prev_start_page = start_page-per_page if start_page-per_page >= 1 else None
    last_page = min(start_page + per_page - 1, paginator.num_pages)
    next_start_page = last_page + 1 if last_page + 1 <= paginator.num_pages else None

    context = {
        'review_list': page_obj,
        'page_range': range(start_page, last_page+1),
        'prev_start_page': prev_start_page,
        'next_start_page': next_start_page,
    }                   

    return render(request, 'main/review_display.html', context)

def inference_thread_func(review, host, port, id, image_bytes):
    result = GrpcClient.inference_request(host, port, id, image_bytes)
    review.food_type = result['food_type']
    review.prob = result['probability']
    review.save()

    # 명시적 종료 안할경우 thread 종료되어도 connection이 남아있음
    db.connections.close_all()