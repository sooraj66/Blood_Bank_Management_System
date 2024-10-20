"""
This module contains serializers for the Blood Bank Management System API.

1. BloodTypeSerializer:
   - Serializes the BloodType model (name).

2. BloodInventorySerializer:
   - Serializes the BloodInventory model (all fields).
   - Converts blood type PK to name for responses.

3. DonorSerializer:
   - Serializes the BloodDonor model (donor_name, blood_type, units_donated, last_donated).

4. BloodRequestSerializer:
   - Serializes the BloodRequest model (all fields).
   - Converts blood type name to PK for requests.

These serializers facilitate data conversion between models and JSON for API requests.
"""

from rest_framework import serializers
from .models import *
from .models import BloodType


class BloodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodType
        fields = ['name']


class BloodInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodInventory
        fields = "__all__"

    # For API responses, converting PK value to corresponding name for readability
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['blood_type'] = instance.blood_type.name
        return representation

    # For POST requests, converting name to corresponding PK value
    def to_internal_value(self, data):
        blood_type_name = data.get('blood_type')

        if not blood_type_name:
            raise serializers.ValidationError({
                'blood_type': 'This field is required.'
            })

        try:
            blood_type = BloodType.objects.get(name=blood_type_name)
            data['blood_type'] = blood_type.id
        except BloodType.DoesNotExist:
            raise serializers.ValidationError({
                'blood_type': f"Blood type '{blood_type_name}' does not exist."
            })

        return super().to_internal_value(data)


class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodDonor
        fields = ['donor_name', 'blood_type', 'units_donated', 'last_donated']

    # For API responses, converting PK value to corresponding name for readability
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['blood_type'] = instance.blood_type.name
        return representation

    # For POST requests, converting name to corresponding PK value
    def to_internal_value(self, data):
        blood_type_name = data.get('blood_type')

        if not blood_type_name:
            raise serializers.ValidationError({
                'blood_type': 'This field is required.'
            })

        try:
            blood_type = BloodType.objects.get(name=blood_type_name)
            data['blood_type'] = blood_type.id
        except BloodType.DoesNotExist:
            raise serializers.ValidationError({
                'blood_type': f"Blood type '{blood_type_name}' does not exist."
            })

        return super().to_internal_value(data)


class BloodRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodRequest
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['blood_type'] = instance.blood_type.name
        return representation

    def to_internal_value(self, data):
        blood_type_name = data.get('blood_type')

        if not blood_type_name:
            raise serializers.ValidationError({
                'blood_type': 'This field is required.'
            })

        try:
            blood_type = BloodType.objects.get(name=blood_type_name)
            data['blood_type'] = blood_type.id
        except BloodType.DoesNotExist:
            raise serializers.ValidationError({
                'blood_type': f"Blood type '{blood_type_name}' does not exist."
            })

        return super().to_internal_value(data)
