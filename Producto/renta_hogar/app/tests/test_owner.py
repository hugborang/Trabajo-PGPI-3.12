from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from app.models import Apartment, ApartmentPhoto, Availability
from PIL import Image
import io
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class OwnerViewsTests(TestCase):

    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer1", 
            email="customer1@example.com", 
            password="password123", 
            role="customer"
        )
        self.owner = User.objects.create_user(
            username="owner1", 
            email="owner1@example.com", 
            password="password123", 
            role="owner"
        )
        self.owner2 = User.objects.create_user(
            username="owner2", 
            email="owner2@example.com",
            password="password123",
            role="owner"
        )
        self.apartment = Apartment.objects.create(
            owner=self.owner,
            address="Apartment 1",
            guest_count=4,
            description="Beautiful apartment",
            is_visible=True,
            price=100
        )
        photo = self.create_test_image()
        ApartmentPhoto.objects.create(apartment=self.apartment, photo=photo)

        self.availability = Availability.objects.create(
            apartment=self.apartment,
            start_date="2024-12-17",
            end_date="2024-12-24",
        )

    @staticmethod
    def create_test_image(name="test.jpg", size=(100, 100), color=(255, 0, 0)):
        file = io.BytesIO()
        image = Image.new("RGB", size, color)
        image.save(file, format="JPEG")
        file.seek(0)
        return SimpleUploadedFile(name, file.read(), content_type="image/jpeg")
    
    def test_onwer_menu(self):
        self.client.login(username="owner1", password="password123")
        response = self.client.get(reverse('owner_menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "owner/owner_menu.html")
        self.assertContains(response, "Apartment 1")

    def test_manage_availability_as_owner(self):
        self.client.login(username="owner1", password="password123")
        response = self.client.get(reverse('manage_availability', args=[self.apartment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "owner/manage_availability.html")
        self.assertContains(response, "Dec. 24, 2024")

    def test_manage_availability_as_customer(self):
        self.client.login(username="customer1", password="password123")
        response = self.client.get(reverse('manage_availability', args=[self.apartment.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "access_denied.html")

    def test_manage_availability_apartment_not_found(self):
        self.client.login(username="owner1", password="password123")
        response = self.client.get(reverse('manage_availability', args=[999]))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")

    def test_manage_availability_foreign_apartment(self):
        self.client.login(username="owner2", password="password123")
        response = self.client.get(reverse('manage_availability', args=[self.apartment.id]))

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "access_denied.html")
