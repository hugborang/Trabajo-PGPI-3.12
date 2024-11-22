# tests/test_reservation.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware, datetime
from app.models import Apartment, Reservation, ApartmentPhoto
from unittest import mock
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

User = get_user_model()

class ReservationTests(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer",
            email="customer@example.com",
            password="password123",
            role="customer"
        )
        self.customer2 = User.objects.create_user(
            username="customer2",
            email="customer2@example.com",
            password="password123",
            role="customer"
        )
        self.owner = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="password123",
            role="owner"
        )
        self.apartment = Apartment.objects.create(
            owner=self.owner,
            address="Test Apartment",
            guest_count=2,
            price=100.00
        )
        photo = self.create_test_image(name="test.jpg")
        ApartmentPhoto.objects.create(apartment=self.apartment, photo=photo)
        self.reservation = Reservation.objects.create(
            cust=self.customer,
            apartment=self.apartment,
            start_date='2024-11-20',
            end_date='2024-11-25'
        )

    @staticmethod
    def create_test_image(name="test.jpg", size=(100, 100), color=(255, 0, 0)):
        file = io.BytesIO()
        image = Image.new("RGB", size, color)
        image.save(file, format="JPEG")
        file.seek(0)
        return SimpleUploadedFile(name, file.read(), content_type="image/jpeg")
    
    def test_create_reservation_as_customer(self):
        self.client.login(username="customer", password="password123")
        response = self.client.post(
            reverse('create_reservation', args=[self.apartment.id]),
            {
                "start_day": "26",
                "start_month": "11",
                "start_year": "2024",
                "end_day": "30",
                "end_month": "11",
                "end_year": "2024",
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Reservation.objects.filter(
            cust=self.customer,
            apartment=self.apartment,
            start_date='2024-11-26',
            end_date='2024-11-30'
        ).exists())


    def test_create_reservation_as_owner(self):
        self.client.login(username="owner", password="password123")
        response = self.client.post(reverse('create_reservation', args=[self.apartment.id]), {
            "start_day": "26",
            "start_month": "11",
            "start_year": "2024",
            "end_day": "30",
            "end_month": "11",
            "end_year": "2024",
        })
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "Solo los inquilinos pueden realizar reservas.", status_code=403)
        self.assertFalse(Reservation.objects.filter(
            cust=self.owner,
            apartment=self.apartment,
            start_date='2024-11-26',
            end_date='2024-11-30'
        ).exists())

    def test_create_reservation_overlapping(self):
        self.client.login(username="customer", password="password123")
        response = self.client.post(reverse('create_reservation', args=[self.apartment.id]), {
            "start_day": "20",
            "start_month": "11",
            "start_year": "2024",
            "end_day": "25",
            "end_month": "11",
            "end_year": "2024",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "El apartamento no está disponible en las fechas seleccionadas.")
        
    def test_create_reservation_invalid_dates(self):
        self.client.login(username="customer", password="password123")
        response = self.client.post(reverse('create_reservation', args=[self.apartment.id]), {
            "start_day": "30",
            "start_month": "11",
            "start_year": "2024",
            "end_day": "26",
            "end_month": "11",
            "end_year": "2024",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "La fecha de inicio debe ser anterior a la fecha de fin.")
        self.assertFalse(Reservation.objects.filter(
            cust=self.customer,
            apartment=self.apartment,
            start_date='2024-11-30',
            end_date='2024-11-26'
        ).exists())

    def test_delete_reservation_as_customer(self):
        self.client.login(username="customer", password="password123")
        response = self.client.post(reverse('delete_reservation', args=[self.reservation.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Reservation.objects.filter(id=self.reservation.id).exists())

    def test_customer_canot_delete_another_customer_reservation(self):
        self.client.login(username="customer2", password="password123")
        response = self.client.post(reverse('delete_reservation', args=[self.reservation.id]))
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "No tienes permiso para cancelar esta reserva.", status_code=403)
        self.assertTrue(Reservation.objects.filter(id=self.reservation.id).exists())
    
    def test_customer_cannot_delete_reservation_a_day_before(self):
        self.client.login(username="customer", password="password123")
        with mock.patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = make_aware(datetime(2024, 11, 19))  # Fecha un día antes del 2024-11-20
            response = self.client.post(reverse('delete_reservation', args=[self.reservation.id]))
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "No se puede cancelar una reserva un día antes de su fecha de inicio.", status_code=403)
        self.assertTrue(Reservation.objects.filter(id=self.reservation.id).exists())
