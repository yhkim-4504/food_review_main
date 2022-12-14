from django.db import models
from django.contrib.auth.models import User

LABEL_TO_IDX = {'': -1, '제육볶음': 0, '김밥': 1, '오무라이스': 2, '돈까스': 3, '라면': 4, '삼계탕': 5, '떡볶이': 6}
IDX_TO_LABEL = {v: k for k, v in LABEL_TO_IDX.items()}

# Create your models here.
class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    food_type = models.CharField(max_length=1, choices=[(str(k), v) for k, v in IDX_TO_LABEL.items()], default=-1)
    rating = models.SmallIntegerField(choices=[(i, i) for i in range(1, 1 + 5)])
    prob = models.FloatField(default=-1)
    create_date = models.DateTimeField()

class ReviewImage(models.Model):
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='review_images/')
    upload_date = models.DateTimeField()