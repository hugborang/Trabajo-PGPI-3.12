# Generated by Django 5.1.1 on 2024-11-10 12:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_customuser_role_apartment_availability'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApartmentPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='apartments/photos')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='app.apartment')),
            ],
        ),
    ]
