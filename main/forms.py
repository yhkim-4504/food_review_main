from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']
        labels = {
            'content': '내용',
            'rating': '별점',
        }