## HOW TO RUN THIS PROJECT
- Install Python(3.12.5)
- Download This Project Zip Folder and Extract it or Clone using git
- Move to project folder in Terminal (Blood_Bank_Management_System). Then run following Commands :

```
python -m pip install -r requirements. txt
```

```
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```
- Now enter following URL in your browser installed on your pc / check corresponding URL endpoints through API testing tool
```
http://127.0.0.1:8000/
```

## API Documentation
### POST http://127.0.0.1:8000/user_register
- **Description:** Allows user to register as admin
- **Request Body:**
  ```json
  {
  "username":"testadmin",
  "email":"testadmin@gmail.com",
  "password":"testadmin",
  "confirmPassword":"testadmin",
  "is_staff":true
  }

- **Response Body:**
  ```json
  {
    "message": "user created successfully",
    "user": {
      "username": "testadmin",
      "email": "testadmin@gmail.com"
    }
  }

### POST http://127.0.0.1:8000/user_register
- **Description:** Allows users to register as regular user.
- **Request Body:**
  ```json
  {
    "username":"testuser",
    "email":"testuser@gmail.com",
    "password":"testuser",
    "confirmPassword":"testuser",
    "is_staff":false
  }
- **Response Body:**
  ```json
  {
    "message": "user created successfully",
    "user": {
      "username": "testuser",
      "email": "testuser@gmail.com"
    }
  }

### POST http://127.0.0.1:8000/user_login
- **Description:** Allows users to login.
- **Request Body:**
  ```json
  {
    "username":"testadmin",
    "password":"testadmin"
  }
- **Response Body:**
  ```json
  {
    "refresh": "refresh_token",
    "access": "access_token",
    "user": {
        "username": "testadmin",
        "email": "testadmin@gmail.com"
    }
  }

### POST http://127.0.0.1:8000/user_logout
- **Description:** Allows users to logout.
- **Request Body:**
  ```json
  {

  }
- **Response Body:**
  ```json
  {
  "message": "Successfully logged out"
  }

### POST http://127.0.0.1:8000/add_bloodtype
- **Description:** Allows admin_user to add blood type.
- **Request Body:**
  ```json
  {
  "name":"AB+"
  }
- **Response Body:**
  ```json
  {
  "message": "Blood type added successfully"
  }

### POST http://127.0.0.1:8000/add_donor
- **Description:** Allows admin_user to add donor.
- **Request Body:**
  ```json
  {
  "donor_name":"Mark",
  "blood_type":"A+",
  "units_donated":3
  }
- **Response Body:**
  ```json
  {
  "message": "Donor added successfully",
  "donor": {
      "donor_name": "Mark",
      "blood_type": "A+",
      "units_donated": 3,
      "last_donated": "2024-10-20"
  }
  }

### PUT http://127.0.0.1:8000/update_donor/{BloodDonor.id}
- **Description:** Allows admin_user to update donor details.
- **Request Body:**
  ```json
  {
  "donor_name":"Siddu",
  "blood_type":"A+",
  "units_donated":3
  }
- **Response Body:**
  ```json
  {
  "message": "Donor details updated successfully"
  }


### DELETE http://127.0.0.1:8000/delete_donor/{BloodDonor.id}
- **Description:** Allows admin_user to delete donor.
- **Request Body:**
  ```json
  {

  }
- **Response Body:**
  ```json
  {
  "message": "Donor deleted successfully"
  }

### GET http://127.0.0.1:8000/getall_donors/?page=2
- **Description:** Allows admin_user to get all donors list.
- **Request Body:**
  ```json
  {

  }
- **Response Body:**
  ```json
  {
  "donors": [
    {
      "donor_name": "Zenda",
      "blood_type": "A+",
      "units_donated": 3,
      "last_donated": "2024-10-20"
    },
    {
      "donor_name": "zid",
      "blood_type": "A-",
      "units_donated": 1,
      "last_donated": "2024-10-19"
    }
  ],
  "total_donors": 7,
  "page": 2,
  "total_pages": 2
  }

### GET http://127.0.0.1:8000/get_bloodinventory
- **Description:** Allows admin_user to get blood inventory .
- **Request Body:**
  ```json
  {

  }
- **Response Body:**
  ```json
  [
    {
      "id": 1,
      "quantity": 3,
      "blood_type": "A+"
    },
    {
      "id": 3,
      "quantity": 4,
      "blood_type": "B-"
    }
  ]
  
### PUT http://127.0.0.1:8000/add_to_bloodinventory
- **Description:** Allows admin_user to update units in blood inventory of particular blood type.
- **Request Body:**
  ```json
  {
  "blood_type":"O+",
  "quantity" : 3
  }
- **Response Body:**
  ```json
  {
    "message": "Blood type with quantity added to inventory",
    "blood_type": {
        "id": 9,
        "quantity": 3,
        "blood_type": "O+"
    }
  }


### PUT http://127.0.0.1:8000/update_units/{bloodType.id}
- **Description:** Allows admin_user to update units in blood inventory of particular blood type.
- **Request Body:**
  ```json
  {
  "blood_type":"AB+",
  "quantity" : 3
  }
- **Response Body:**
  ```json
  {
  "message": "Units available updated"
  }


### POST http://127.0.0.1:8000/request_blood
- **Description:** Allows regular_user to request blood.
- **Request Body:**
  ```json
  {
  "blood_type" : "A+",
  "units_requested":2
  }
- **Response Body:**
  ```json
  {
  "message": "Request successfully send"
  }

### POST http://127.0.0.1:8000/approve_request/{bloodRequest.id}
- **Description:** Allows admin_user to approve request.
- **Request Body:**
  ```json
  {
  "blood_type": "B-",
  "status":true
  }
- **Response Body:**
  ```json
  {
  "message": " Request successfully approved"
  }

### GET http://127.0.0.1:8000/get_all_blood_request/
- **Description:** Allows admin_user to get all list of blood request.
- **Request Body:**
  ```json
  {

  }
- **Response Body:**
  ```json
  {
  "blood_requests": [
    {
      "id": 1,
      "units_requested": 2,
      "status": "Fullfilled",
      "user": 1,
      "blood_type": "A+"
    },
    {
      "id": 2,
      "units_requested": 2,
      "status": "Fullfilled",
      "user": 2,
      "blood_type": "A-"
    },
    {
      "id": 3,
      "units_requested": 2,
      "status": "Fullfilled",
      "user": 3,
      "blood_type": "A-"
    },
    {
      "id": 4,
      "units_requested": 2,
      "status": "Pending",
      "user": 5,
      "blood_type": "A+"
    }
  ],
  "total_request": 4,
  "page": 1,
  "total_pages": 1
  }