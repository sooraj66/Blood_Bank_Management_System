"""
Models for the Blood Bank Management System.

1. BloodType: Represents different blood types, with choices including A+, A-, B+, B-, AB+, AB-, O+, and O-.
2. BloodInventory: Tracks the inventory of blood types, linking to BloodType and storing the available quantity.
3. BloodDonor: Stores information about blood donors, including their name, blood type, units donated, and last donation date.
4. BloodRequest: Records requests made by users for specific blood types and quantities, along with the request status.
"""

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator


class BloodType(models.Model):  # Model for storing  blood types
    BLOOD_TYPE_CHOICES = [
        ('A+', 'add_to_bloodinventory'),
        ('A-', 'A Negative'),
        ('B+', 'B Positive'),
        ('B-', 'B Negative'),
        ('AB+', 'AB Positive'),
        ('AB-', 'AB Negative'),
        ('O+', 'O Positive'),
        ('O-', 'O Negative'),
    ]
    name = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, unique=True)

    def __str__(self):
        return self.nameD


class BloodInventory(models.Model):  # Model for storing available blood types with units available
    blood_type = models.OneToOneField(BloodType, on_delete=models.CASCADE, unique=True)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.blood_type.name} - {self.quantity} units"


class BloodDonor(models.Model):  # Model for storing blood donor details
    donor_name = models.CharField(max_length=20, null=False, unique=True)
    blood_type = models.ForeignKey(BloodType, on_delete=models.CASCADE, blank=False, null=False)
    units_donated = models.IntegerField(blank=True, null=True)
    last_donated = models.DateField(null=True, blank=True)


class BloodRequest(models.Model):  # Model for storing blood request made by regular users
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_type = models.ForeignKey(BloodType, on_delete=models.CASCADE)
    units_requested = models.IntegerField()
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Request by {self.user.username} for {self.units_requested} units of {self.blood_type.name}"
