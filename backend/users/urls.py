from django.urls import path
from .views import (
    register, 
    login, 
    forgot, 
    user_list_create, 
    user_detail, 
    create_disaster,
    get_all_disasters,
    get_disaster_by_name,
    update_disaster_by_name,
    delete_disaster_by_name,
    get_all_cities,
    create_city,
    get_city,
    update_city,
    delete_city,
    get_disaster_info,
    index,
    add_notification, get_notifications, delete_notification,delete_disaster_by_name, update_disaster_by_name,
     get_rescue_data
)

urlpatterns = [
    # User Authentication Endpoints
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('forgot/', forgot, name='forgot-password'),

    # User CRUD Endpoints
    path('users/', user_list_create, name='user-list-create'),
    path('users/<int:pk>/', user_detail, name='user-detail'),

    # Disaster CRUD Endpoints
    path('disasters/', get_all_disasters, name='get_all_disasters'),  # GET all disasters
    path('disasters/create/', create_disaster, name='create_disaster'),  # POST - Create a new disaster
    path('disasters/<str:name>/', get_disaster_by_name, name='get_disaster_by_name'),  # GET - Get a disaster by Name
    path('disasters/update/<str:name>/', update_disaster_by_name, name='update_disaster_by_name'),  # PUT/PATCH - Update by Name
    path('disasters/delete/<str:name>/', delete_disaster_by_name, name='delete_disaster_by_name'),  # DELETE - Delete by Name

    path('cities/', get_all_cities, name='get_all_cities'),
    path('cities/create/', create_city, name='create_city'),
    path('cities/<int:pk>/', get_city, name='get_city'),
    path('cities/update/<int:pk>/', update_city, name='update_city'),
    path('cities/delete/<int:pk>/', delete_city, name='delete_city'),

    path('disaster/<str:disaster_name>/', get_disaster_info, name='get_disaster_info'),
    path('', index, name='index'), 

    path("add-alert/", add_notification, name="add-alert"),
    path("get-alerts/", get_notifications, name="get-alerts"),
    path('delete-alerts/<int:id>/', delete_notification, name='delete_notification'),

     path('rescue-data/', get_rescue_data, name='get_rescue_data'),

]

