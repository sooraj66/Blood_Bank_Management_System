"""
URL configuration for bloodbank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Urls for Registration, Login, Logout
    path('user_register', views.user_register, name='user_register'),
    path('user_login', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),

    # Url for adding blood type to database
    path('add_bloodtype', views.add_blood_type, name='add_blood_type'),

    # Urls for Adding, Updating, Deleting, Fetching from BloodDonor
    path('add_donor', views.add_donor, name='add_donor'),
    path('update_donor/<int:id>', views.update_donor, name='update_donor'),
    path('delete_donor/<int:id>', views.delete_donor, name='delete_donor'),
    path('getall_donors/', views.get_all_donors, name='get_all_donors'),

    # Urls for Adding, Updating, Fetching from BloodInventory
    path('get_bloodinventory', views.get_blood_inventory, name='get_blood_inventory'),
    path('add_to_bloodinventory', views.add_to_bloodinventory, name='add_to_bloodinventory'),
    path('update_units/<int:id>', views.update_bloodinventory, name='update_bloodinventory'),

    # Url for Requesting Blood fro regular users
    path('request_blood', views.request_blood, name='request_blood'),

    # Urls for Fetching and Approving Blood Requestslogout
    path('get_all_blood_request/', views.view_all_bloodrequest, name='view_all_bloodrequest'),
    path('approve_request/<int:id>', views.approve_request, name='approve_request')
]
