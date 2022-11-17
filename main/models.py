from django.db import models

# Create your models here.
class Review(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='review_images/', blank=True, null=True)
    create_date = models.DateTimeField()
