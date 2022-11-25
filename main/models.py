from django.db import models

LABEL_TO_IDX = {'': -1, '제육볶음': 0, '김밥': 1, '오무라이스': 2, '돈까스': 3, '라면': 4, '삼계탕': 5, '떡볶이': 6}
IDX_TO_LABEL = {v: k for k, v in LABEL_TO_IDX.items()}

# Create your models here.
class Review(models.Model):
    content = models.TextField()
    food_type = models.CharField(max_length=1, choices=[(k, v) for k, v in IDX_TO_LABEL.items()], default=-1)
    create_date = models.DateTimeField()

class ReviewImage(models.Model):
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='review_images/')
    upload_date = models.DateTimeField()