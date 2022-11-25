import threading
from django import db
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .models import ReviewImage
from .forms import ReviewForm
from grpc_ai_client.ai_client import GrpcClient

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

        return render(request, 'main/review_create.html')
    else:
        form = ReviewForm()
        context = {
            'form': form
        }

        return render(request, 'main/review_create.html', context)

def inference_thread_func(review, host, port, id, image_bytes):
    result = GrpcClient.inference_request(host, port, id, image_bytes)
    review.food_type = result['food_type']
    review.prob = result['probability']
    review.save()

    # 명시적 종료 안할경우 thread 종료되어도 connection이 남아있음
    db.connections.close_all()