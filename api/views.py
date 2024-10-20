from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .serializers import *
from datetime import date


# Create your views here.
@api_view(['POST'])
def user_register(request):  # Function for new user registration
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    confirmPassword = request.data.get('confirmPassword')
    is_staff = request.data.get('is_staff')

    if User.objects.filter(Q(username=username) | Q(email=email)).exists():
        return Response({'error': 'Username or email already exist'}, status=status.HTTP_400_BAD_REQUEST)

    if password != confirmPassword:
        return Response({'error': 'password doesnt match'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(
        username=username,
        email=email,
        is_staff=bool(is_staff),
    )
    user.set_password(password),
    user.save()
    return Response({
        'message': "user created successfully",
        'user': {
            'username': username,
            'email': email
        }
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def user_login(request):  # Function for user login
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token, ), 'user': {
                'username': user.username,
                'email': user.email
            }
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    try:
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_blood_type(request):
    if request.user.is_staff:
        serializer = BloodTypeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Blood type added successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Only admin can add blood type'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_donors(request):  # Function to  get all list of donor
    if request.user.is_staff:
        page = request.GET.get('page', 1)
        query = request.GET.get('q', '')
        donors_list = BloodDonor.objects.all()

        if query:  # Included search functionality
            donors_list = donors_list.filter(blood_type__name__icontains=query.strip())

        donors = donors_list.order_by("-last_donated")

        total_donors = donors.count()

        donor_paginator = Paginator(donors, 5)  # Pagination included for list of donors greater than 10 sets
        paginated_donors_list = donor_paginator.get_page(page)

        serializer = DonorSerializer(paginated_donors_list, many=True)
        json_data = {
            'donors': serializer.data,
            'total_donors': total_donors,
            'page': paginated_donors_list.number,
            'total_pages': donor_paginator.num_pages
        }
        return Response(json_data, status=status.HTTP_200_OK)
    else:
        return Response({"message": "List of donors can only be viewed by admin"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_donor(request):  # Function to Add a new donor
    if request.user.is_staff:
        serializer = DonorSerializer(data=request.data)

        if serializer.is_valid():
            donor = serializer.save()
            donor.last_donated = date.today()
            donor.save()
            return Response({"message": "Donor added successfully", "donor": serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Only admin can add donor'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
def update_donor(request, id):  # Function to update current donor details
    if request.user.is_staff:
        donor = get_object_or_404(BloodDonor, pk=id)
        serializer = DonorSerializer(instance=donor, data=request.data, partial=True)

        if serializer.is_valid():
            donor = serializer.save()
            donor.last_donated = date.today()
            donor.save()
            return Response({"message": "Donor details updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Only admin can add donor'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_donor(request, id):  # Function to delete existing donor
    if request.user.is_staff:
        donor = get_object_or_404(BloodDonor, pk=id)
        donor.delete()
        return Response({'message': 'Donor deleted successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Only admin can delete donor'}, status=status.HTTP_403_FORBIDDEN)


# Function to get all blood types in inventory and respected units available (*accessed by admin and users)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_blood_inventory(request):
    blood_inventory = BloodInventory.objects.all()
    serializer = BloodInventorySerializer(blood_inventory, many=True)
    json_data = serializer.data
    return Response(json_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_bloodinventory(request):  # Function to Add to blood inventory
    if request.user.is_staff:
        serializer = BloodInventorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Blood type with quantity added to inventory', 'blood_type': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Only admin can Add to Blood Inventory'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_bloodinventory(request, id):  # Function to update units available to corresponding blood type
    if request.user.is_staff:
        blood_type = get_object_or_404(BloodInventory, pk=id)
        serializer = BloodInventorySerializer(instance=blood_type, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"Units available updated"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Only admin can update Blood Inventory'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_blood(request):  # Function for Requesting Blood
    if not request.user.is_staff:
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = BloodRequestSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Request successfully send'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "Blood request can be initiated by users only"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_all_bloodrequest(request):
    if request.user.is_staff:
        page = request.GET.get('page', 1)
        query = request.GET.get('q', '')
        request_list = BloodRequest.objects.all()

        if query:
            request_list = request_list.filter(status__icontains=query)  # Included search functionality

        total_requests = request_list.count()

        blood_request_paginator = Paginator(request_list, 5)  # Pagination included for list of blood request
        paginated_blood_requests = blood_request_paginator.get_page(page)

        serializer = BloodRequestSerializer(paginated_blood_requests, many=True)
        json_data = {
            'blood_requests': serializer.data,
            'total_request': total_requests,
            'page': paginated_blood_requests.number,
            'total_pages': blood_request_paginator.num_pages
        }
        return Response(json_data, status=status.HTTP_200_OK)
    else:
        return Response({
            "message": "list of blood request can only be viewed by admin"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_request(request, id):
    if request.user.is_staff:
        blood_request = get_object_or_404(BloodRequest, pk=id)

        if not request.data:
            return Response({"message": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)

        if not request.data['status']:
            return Response({"message": "Request cancelled"}, status=status.HTTP_200_OK)

        request.data['status'] = 'Fulfilled'  # Status of request changing from Pending to Fulfilled if Status is True

        serializer = BloodRequestSerializer(instance=blood_request, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": " Request successfully approved"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "Blood Request can only be approved by admin"},
                        status=status.HTTP_403_FORBIDDEN)
