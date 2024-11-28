from django.test import TestCase, Client
from django.urls import reverse
from app.models import Apartment, CustomUser, Reservation, Availability
from datetime import datetime, timedelta
import json
from unittest.mock import patch

class CreateReservationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = CustomUser.objects.create_user(username='customer', password='password123', email='customer@example.com', role='customer')
        self.owner = CustomUser.objects.create_user(username='owner', password='password123', email='owner@example.com', role='owner')
        self.apartment = Apartment.objects.create(owner=self.owner, address='Calle Test, 123', price=100, guest_count=2, is_visible=True)
        self.availability = Availability.objects.create(apartment=self.apartment, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=30))
        self.reservation = Reservation.objects.create(
            cust=self.customer,
            apartment=self.apartment,
            start_date=datetime.now() + timedelta(days=5),
            end_date=datetime.now() + timedelta(days=10),
            total_price=500
        )
        self.url = reverse('delete_reservation', args=[self.reservation.id])
        

    def test_get_create_reservation(self):
        self.client.login(username='customer', password='password123')
        response = self.client.get(reverse('create_reservation', args=[self.apartment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Calle Test, 123')

    def test_post_create_reservation_success(self):
        self.client.login(username='customer', password='password123')
        start_date = (datetime.now() + timedelta(days=12)).strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')
        response = self.client.post(reverse('create_reservation', args=[self.apartment.id]), {
            'start_date': start_date,
            'end_date': end_date
        })
        self.assertEqual(response.status_code, 302)

    def test_post_create_reservation_conflict(self):
        self.client.login(username='customer', password='password123')
        response = self.client.post(reverse('create_reservation', args=[self.apartment.id]), {
            'start_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=12)).strftime('%Y-%m-%d')
        })
        self.assertContains(response, 'El apartamento no está disponible')

    def test_post_create_reservation_invalid_apartment(self):
        self.client.login(username='customer', password='password123')
        response = self.client.post(reverse('create_reservation', args=[9999]), {
            'start_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=12)).strftime('%Y-%m-%d')
        })
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_verify_payment_failure(self):
        self.client.login(username='customer', password='password123')
        response = self.client.get(reverse('verify_payment'), {'session_id': 'invalid_session'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/payment_failed.html')

    def test_delete_reservation_success(self):
        self.client.login(username='customer', password='password123')
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('manage_reservations'))
        self.assertFalse(Reservation.objects.filter(id=self.reservation.id).exists())

    def test_delete_reservation_not_owner(self):
        another_customer = CustomUser.objects.create_user(username='another', password='password123', email='another@example.com', role='customer')
        self.client.login(username='another', password='password123')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

    def test_delete_reservation_get_request(self):
        self.client.login(username='customer', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/manage_reservations.html')
