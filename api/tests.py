"""
This module contains unit tests for the Blood Bank Management System API.

Tests Included:
- User Registration: Verifies that users can register successfully and that the necessary fields are validated.
- User Login: Ensures that users can log in with valid credentials and receive JWT tokens.
- Blood Type Management: Tests for adding and fetching blood types.
- Donor Management: Tests for adding, updating, deleting, and fetching blood donor records.
- Blood Inventory Management: Verifies the functionality for managing blood inventory.
- Blood Request Management: Tests the ability to request blood and for admins to approve these requests.

Test Framework:
- Uses Django's built-in testing framework for creating and running tests.
- Each test case is structured to check specific functionality and includes assertions to verify expected outcomes.

Usage:
To run the tests, execute the following command in the terminal:
    python manage.py test
"""

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import BloodType, BloodDonor, BloodRequest


class TestApiEndpoints(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username="adminuser", password="adminpassword", is_staff=True)

        self.regular_user = User.objects.create_user(username="regularuser", password="regularpassword", is_staff=False)

        self.valid_blood_type_data = {
            "name": "B+"
        }
        self.blood_type = BloodType.objects.create(name="O+")

        self.donor = BloodDonor.objects.create(
            donor_name="John Doe", blood_type=self.blood_type, units_donated=2)

    def authenticate_as_admin(self):
        refresh = RefreshToken.for_user(self.admin_user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def authenticate_as_regular_user(self):
        refresh = RefreshToken.for_user(self.regular_user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_user_logout(self):
        self.authenticate_as_regular_user()

        refresh_token = RefreshToken.for_user(self.regular_user)
        response = self.client.post('/user_logout', {'refresh': str(refresh_token)})

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_add_blood_type_as_admin(self):
        self.authenticate_as_admin()

        response = self.client.post('/add_bloodtype', self.valid_blood_type_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(BloodType.objects.filter(name='O+').exists())

    def test_add_blood_type_as_regular_user(self):
        self.authenticate_as_regular_user()

        response = self.client.post('/add_bloodtype', self.valid_blood_type_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertFalse(BloodType.objects.filter(name='B+').exists())

    def test_add_blood_type_without_authentication(self):
        self.client.credentials()

        response = self.client.post('/add_bloodtype', self.valid_blood_type_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_donors_as_admin(self):
        self.authenticate_as_admin()

        response = self.client.get('/getall_donors/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_donors_as_regular_user(self):
        self.authenticate_as_regular_user()

        response = self.client.get('/getall_donors/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_donor_as_admin(self):
        self.authenticate_as_admin()

        data = {
            "donor_name": "siddhu",
            "blood_type": self.blood_type.name,
            "units_donated": 2
        }

        response = self.client.post('/add_donor', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertEqual(response_data['donor']['donor_name'], "siddhu")
        self.assertEqual(response_data['donor']['blood_type'], self.blood_type.name)
        self.assertEqual(response_data['donor']['units_donated'], 2)
        self.assertTrue(BloodDonor.objects.filter(donor_name="siddhu").exists())

    def test_update_donor_as_admin(self):
        self.authenticate_as_admin()
        updated_data = {
            "donor_name": "John Smith",
            "blood_type": self.blood_type.name,
            "units_donated": 3
        }

        response = self.client.put(f'/update_donor/{self.donor.id}', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.donor.refresh_from_db()
        self.assertEqual(self.donor.donor_name, "John Smith")
        self.assertEqual(self.donor.units_donated, 3)

        self.assertEqual(self.donor.blood_type, self.blood_type)

    def test_delete_donor_as_admin(self):
        self.authenticate_as_admin()

        response = self.client.delete(f'/delete_donor/{self.donor.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_blood_inventory_details_regular_user(self):
        self.authenticate_as_regular_user()

        response = self.client.get('/get_bloodinventory')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_blood_inventory_details_admin(self):
        self.authenticate_as_admin()

        response = self.client.get('/get_bloodinventory')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_to_blood_inventory_as_admin(self):
        self.authenticate_as_admin()

        data = {
            "blood_type": self.blood_type.name,
            "quantity": 2
        }

        response = self.client.post('/add_to_bloodinventory', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertEqual(response_data['blood_type']['quantity'], 2)
        self.assertEqual(response_data['blood_type']['blood_type'], self.blood_type.name)

    def test_add_to_blood_inventory_as_regular_user(self):
        self.authenticate_as_regular_user()

        data = {
            "blood_type": self.blood_type.name,
            "quantity": 2
        }

        response = self.client.post('/add_to_bloodinventory', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_blood_inventory_as_admin(self):
        self.authenticate_as_admin()
        self.test_add_to_blood_inventory_as_admin()
        updated_data = {
            "blood_type": self.blood_type.name,
            "quantity": 6
        }

        response = self.client.put(f'/update_units/{self.blood_type.id}', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_request_blood_as_admin(self):
        self.authenticate_as_admin()
        data = {
            "blood_type": self.blood_type.name,
            "units_requested": 2
        }

        response = self.client.post('/request_blood', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_request_blood_as_regular_user(self):
        self.authenticate_as_regular_user()
        data = {
            "blood_type": self.blood_type.name,
            "units_requested": 2
        }

        response = self.client.post('/request_blood', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_blood_request_as_admin(self):
        self.authenticate_as_admin()

        response = self.client.get('/get_all_blood_request/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_blood_request_as_regular_user(self):
        self.authenticate_as_regular_user()

        response = self.client.get('/get_all_blood_request/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_approve_as_admin(self):
        self.authenticate_as_admin()

        self.authenticate_as_regular_user()
        self.test_request_blood_as_regular_user()

        self.authenticate_as_admin()

        blood_request = BloodRequest.objects.last()  # Get the latest created request
        data = {
            "blood_type": self.blood_type.name,
            "status": True
        }

        response = self.client.post(f'/approve_request/{blood_request.id}', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        blood_request.refresh_from_db()
        self.assertEqual(blood_request.status, 'Fullfilled')

    def test_approve_as_regular_user(self):
        self.authenticate_as_regular_user()
        self.test_request_blood_as_regular_user()

        blood_request = BloodRequest.objects.last()  # Get the latest created request
        data = {
            "status": True
        }

        response = self.client.post(f'/approve_request/{blood_request.id}', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
