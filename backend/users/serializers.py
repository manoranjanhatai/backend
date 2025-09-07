from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User ,Disaster ,City ,Disasterchatbot,Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class DisasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disaster
        fields = ['name', 'description', 'precautions']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'cityName', 'subcity', 'route', 'contact', 'services']   

class DisasterSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Disasterchatbot
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
