from django.test import TestCase
from django.urls import reverse
from app.models import Apartment, CustomUser, Review, ApartmentPhoto, Availability, Reservation
from app.forms.review_form import ReviewForm
from freezegun import freeze_time
import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

class ReviewTests(TestCase):
    def setUp(self):
        self.owner = CustomUser.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="password123",
            role="owner"
        )
        self.customer = CustomUser.objects.create_user(
            username="customer",
            email="customer@example.com",
            password="password123",
            role="customer"
        )
        self.apartment = Apartment.objects.create(
            owner=self.owner,
            address="123 Test St",
            guest_count=4,
            description="A beautiful apartment",
            price=100.0,
            is_visible=True,
        )
        photo = self.create_test_image()
        ApartmentPhoto.objects.create(apartment=self.apartment, photo=photo)

        Availability.objects.create(
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

    def test_create_reviews_get(self):
        self.client.login(username="customer", password="password123")
        response = self.client.get(reverse('create_review', args=[self.apartment.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customer/review_form.html")
        self.assertIsInstance(response.context['form'], ReviewForm)

    @freeze_time("2024-12-26")
    def test_create_reviews_post_valid(self):
        self.client.login(username="customer", password="password123")
        Reservation.objects.create(cust=self.customer, apartment=self.apartment, start_date="2024-12-19", end_date="2024-12-22", total_price=300)
        data = {
            'rating': 5,
            'comment': "Great stay!"
        }
        response = self.client.post(reverse('create_review', args=[self.apartment.id]), data)

        self.assertRedirects(response, reverse('customer_menu'))
        self.assertTrue(Review.objects.filter(user=self.customer, apartment=self.apartment).exists())

    @freeze_time("2024-12-23")
    def test_create_reviews_duplicate_review(self):
        self.client.login(username="customer", password="password123")
        Reservation.objects.create(cust=self.customer, apartment=self.apartment, start_date="2024-12-19", end_date="2024-12-22", total_price=300)
        Review.objects.create(user=self.customer, apartment=self.apartment, rating=5, comment="Nice place!")
        data = {
            'rating': 4,
            'comment': "Another review"
        }
        response = self.client.post(reverse('create_review', args=[self.apartment.id]), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customer/review_form.html")
        self.assertContains(response, "Ya has dejado una valoración para este apartamento.")
        self.assertEqual(Review.objects.filter(user=self.customer, apartment=self.apartment).count(), 1)

    @freeze_time("2024-12-19")
    def test_create_reviews_during_reservation(self):
        self.client.login(username="customer", password="password123")
        Reservation.objects.create(cust=self.customer, apartment=self.apartment, start_date="2024-12-19", end_date="2024-12-22", total_price=300)
        data = {
            'rating': 5,
            'comment': "Great stay!"
        }
        response = self.client.post(reverse('create_review', args=[self.apartment.id]), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customer/review_form.html")
        self.assertContains(response, "La reserva debe haber finalizado para dejar una valoración.")
        self.assertFalse(Review.objects.filter(user=self.customer, apartment=self.apartment).exists())

    def test_create_reviews_apartment_not_found(self):
        self.client.login(username="customer", password="password123")
        invalid_url = reverse('create_review', args=[999])  # Non-existent apartment ID
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")

    @freeze_time("2024-12-26")
    def test_aparment_review(self):
        self.client.login(username="customer", password="password123")
        Review.objects.create(user=self.customer, apartment=self.apartment, rating=5, comment="Nice place!")
        self.client.logout()
        self.client.login(username="owner", password="password123")
        response = self.client.get(reverse('owner_review'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "owner/review_list.html")
        self.assertContains(response, "Nice place!")
   