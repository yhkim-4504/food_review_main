from django.db import models

# Create your models here.
class Review(models.Model):
    content = models.TextField()
    create_date = models.DateTimeField()

class ReviewImage(models.Model):
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='review_images/')
    upload_date = models.DateTimeField()