# Generated by Django 5.1 on 2024-10-19 11:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_blooddonor_donor_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodinventory',
            name='blood_type',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.bloodtype'),
        ),
    ]
