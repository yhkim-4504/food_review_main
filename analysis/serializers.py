from rest_framework import serializers
from django.contrib.auth.models import User
from common.models import UserInfo
from main.models import Review

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('gender', 'birthday')

class UserSerializer(serializers.ModelSerializer):
    userinfo = UserInfoSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ('userinfo',)
        
class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ('author', 'food_type', 'rating', 'create_date')
        
