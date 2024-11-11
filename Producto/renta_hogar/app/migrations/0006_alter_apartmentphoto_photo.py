# Generated by Django 5.1.1 on 2024-11-11 20:46

import app.models.apartmentPhoto
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_apartment_address_alter_apartment_guest_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartmentphoto',
            name='photo',
            field=models.ImageField(upload_to='apartments/photos', validators=[app.models.apartmentPhoto.validate_image_extension], verbose_name='Foto del apartamento'),
        ),
    ]