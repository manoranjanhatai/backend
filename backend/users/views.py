from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import csv
import os
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User ,Disaster,City,Review
from .serializers import UserSerializer ,DisasterSerializer ,CitySerializer,ReviewSerializer
from .disaster_models import DisasterAlert
from django.shortcuts import get_object_or_404

# Add a new review
@api_view(['POST'])
def add_review(request):
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve all reviews
@api_view(['GET'])
def get_reviews(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Retrieve a single review by ID
@api_view(['GET'])
def get_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    serializer = ReviewSerializer(review)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Update a review (PUT)
@api_view(['PUT'])
def update_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    serializer = ReviewSerializer(review, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Partially update a review (PATCH)
@api_view(['PATCH'])
def partial_update_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    serializer = ReviewSerializer(review, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete a review
@api_view(['DELETE'])
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    return Response({"message": "Review deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            phone = data.get('phone')
            name = data.get('name')
            password = data.get('password')
            role = data.get('role', 'user')  # Default role

            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'User already exists'}, status=400)

            # Create user with hashed password
            user = User.objects.create_user(email=email, phone=phone, name=name, password=make_password(password), role=role)
            
            return JsonResponse({'message': 'User registered successfully', 'role': user.role})
        except Exception as e:
            return JsonResponse({'error': 'Something went wrong', 'details': str(e)}, status=500)

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from .models import User  # Ensure correct model import

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')  # Ensure correct encoding
            data = json.loads(body_unicode)  # Parse JSON
            
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({'error': 'Email and password are required'}, status=400)

            user = User.objects.filter(email=email).first()
            if user:
                # 1. First, check if password matches hashed version
                if check_password(password, user.password) or user.password == password:
                    return JsonResponse({
                        'message': 'Login successful',
                        'name': user.name,
                        'email': user.email,
                        'phone': user.phone,
                        'role': user.role
                    })
                else:
                    return JsonResponse({'error': 'Invalid email or password'}, status=400)
            
            return JsonResponse({'error': 'User not found'}, status=400)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format', 'details': str(e)}, status=400)

        except Exception as e:
            return JsonResponse({'error': 'Something went wrong', 'details': str(e)}, status=500)


@csrf_exempt
def forgot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            new_password = data.get('newPassword')

            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({'error': 'User not found'}, status=400)

            # Hash new password before saving
            user.password = make_password(new_password)
            user.save()

            return JsonResponse({'message': 'Password changed successfully!'})
        except Exception as e:
            return JsonResponse({'error': 'Something went wrong', 'details': str(e)}, status=500)


@api_view(['GET', 'POST'])
def user_list_create(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, Update, and Delete a User
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Disaster
from .serializers import DisasterSerializer


@api_view(['POST'])
def create_disaster(request):
    serializer = DisasterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get All Disasters
@api_view(['GET'])
def get_all_disasters(request):
    disasters = Disaster.objects.all()
    serializer = DisasterSerializer(disasters, many=True)
    return Response(serializer.data)

# Get Disaster by Name
@api_view(['GET'])
def get_disaster_by_name(request, name):
    try:
        disaster = Disaster.objects.get(name=name)
        serializer = DisasterSerializer(disaster)
        return Response(serializer.data)
    except Disaster.DoesNotExist:
        return Response({"error": "Disaster Not Found"}, status=status.HTTP_404_NOT_FOUND)

# Update Disaster by Name
@api_view(['PUT', 'PATCH'])
def update_disaster_by_name(request, name):
    try:
        disaster = Disaster.objects.get(name=name)
        serializer = DisasterSerializer(disaster, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Disaster.DoesNotExist:
        return Response({"error": "Disaster Not Found"}, status=status.HTTP_404_NOT_FOUND)

# Delete Disaster by Name
@api_view(['DELETE'])
def delete_disaster_by_name(request, name):
    try:
        disaster = Disaster.objects.get(name=name)
        disaster.delete()
        return Response({"message": "Disaster deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Disaster.DoesNotExist:
        return Response({"error": "Disaster Not Found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_city(request):
    serializer = CitySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve all cities (GET)
@api_view(['GET'])
def get_all_cities(request):
    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Retrieve a single city by ID (GET)
@api_view(['GET'])
def get_city(request, pk):
    try:
        city = City.objects.get(pk=pk)
        serializer = CitySerializer(city)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except City.DoesNotExist:
        return Response({"error": "City not found"}, status=status.HTTP_404_NOT_FOUND)

# Update a city by ID (PUT/PATCH)
@api_view(['PUT', 'PATCH'])
def update_city(request, pk):
    try:
        city = City.objects.get(pk=pk)
    except City.DoesNotExist:
        return Response({"error": "City not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CitySerializer(city, data=request.data, partial=True)  # Use partial=True for PATCH
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete a city by ID (DELETE)
@api_view(['DELETE'])
def delete_city(request, pk):
    try:
        city = City.objects.get(pk=pk)
        city.delete()
        return Response({"message": "City deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except City.DoesNotExist:
        return Response({"error": "City not found"}, status=status.HTTP_404_NOT_FOUND)

def load_disasters():
    disaster_dict = {}
    csv_file_path = os.path.join(settings.BASE_DIR, 'users', 'disasters.csv')    
    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                disaster_name = row['name'].strip().capitalize()  # Normalize name
                disaster_dict[disaster_name] = {
                    "name": disaster_name,
                    "description": row.get("description", "No description available."),
                    "causes": row.get("causes", "").split(";"),  # Assuming causes are separated by ;
                    "precautions": row.get("precautions", "").split(";"),
                    "reference_links": row.get("reference_links", "").split(";"),
                }
    except FileNotFoundError:
        print("⚠️ CSV file not found!")

    return disaster_dict


# 🔹 Load disasters when the server starts
disasters = load_disasters()

# 🔹 Default API response
def index(request):
    return JsonResponse({"message": "Welcome to the Disaster Chatbot API"})

# 🔹 Fetch disaster details
def get_disaster_info(request, disaster_name):
    disaster_name = disaster_name.capitalize()  # Normalize case
    if disaster_name in disasters:
        return JsonResponse(disasters[disaster_name])
    else:
        return JsonResponse({"error": "Disaster not found"}, status=404)



@csrf_exempt
def add_notification(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message")

            if not message:
                return JsonResponse({"error": "Message is required"}, status=400)

            # ✅ Correct field names
            cities = City.objects.values_list("cityName", flat=True)  # Use 'cityName' instead of 'name'
            subcities = City.objects.values_list("subcity", flat=True)  # Subcities
            all_locations = set(cities) | set(subcities)  # Combine both

            # ✅ Save the notification
            notification = DisasterAlert.objects.create(message=message)

            return JsonResponse({"message": "Notification added successfully", "id": notification.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def get_notifications(request):
    notifications = DisasterAlert.objects.order_by("-timestamp")[:10]
    data = [
        {"id": notification.id, "message": notification.message, "timestamp": notification.timestamp.strftime("%Y-%m-%d %H:%M:%S")}
        for notification in notifications
    ]
    return JsonResponse({"notifications": data}, safe=False)

@csrf_exempt
def delete_notification(request, id):
    if request.method == "DELETE":
        try:
            notification = DisasterAlert.objects.get(id=id)
            notification.delete()
            return JsonResponse({"message": "Notification deleted successfully"}, status=200)
        except DisasterAlert.DoesNotExist:
            return JsonResponse({"error": "Notification not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)

import re
def get_rescue_data(request):
    notifications = DisasterAlert.objects.values_list("message", flat=True)  # ✅ Get only messages
    cities = City.objects.values("cityName", "subcity", "contact", "route", "services")  

    all_locations = {city["cityName"] for city in cities if city["cityName"]} | \
                    {city["subcity"] for city in cities if city["subcity"]}

    # ✅ Identify locations present in notifications
    excluded_locations = set()
    for message in notifications:
        message_lower = message.lower()
        for loc in all_locations:
            if loc and loc.lower() in message_lower:
                excluded_locations.add(loc)

    # ✅ Filter out cities where cityName or subcity is in excluded_locations
    filtered_cities = [
        city for city in cities if city["cityName"] not in excluded_locations and city["subcity"] not in excluded_locations
    ]

    # ✅ Prepare response data
    rescue_data = [
        {
            "cityName": city["cityName"],
            "subcity": city["subcity"],
            "contact": city["contact"],
            "route": city["route"],
            "services": city["services"]
        }
        for city in filtered_cities
    ]

    return JsonResponse({"rescue_data": rescue_data}, safe=False)
