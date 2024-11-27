from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from app.models import Apartment, CustomUser, Availability, Reservation

class CustomerMenuTests(TestCase):
    def setUp(self):
        # Crear usuarios
        self.owner = CustomUser.objects.create_user(username='owner', password='password123', email='owner@example.com', role='owner')
        self.customer = CustomUser.objects.create_user(username='customer', password='password123', email='customer@example.com', role='customer')

        # Crear apartamentos del propietario
        self.apartment1 = Apartment.objects.create(owner=self.owner, address='Apartment 1', guest_count=2, price=100, is_visible=True)
        self.apartment2 = Apartment.objects.create(owner=self.owner, address='Apartment 2', guest_count=4, price=150, is_visible=True)
        self.apartment3 = Apartment.objects.create(owner=self.owner, address='Apartment 3', guest_count=6, price=200, is_visible=False)
        self.apartment4 = Apartment.objects.create(owner=self.owner, address='Apartment 4', guest_count=1, price=50, is_visible=True)

        # Crear disponibilidades para los apartamentos
        Availability.objects.create(apartment=self.apartment1, start_date='2024-12-17', end_date='2024-12-20')
        Availability.objects.create(apartment=self.apartment2, start_date='2024-12-23', end_date='2024-12-28')

        # Crear reservas para los apartamentos
        Reservation.objects.create(
            cust=self.customer,
            apartment=self.apartment1,
            start_date='2024-12-18',
            end_date='2024-12-20',
            total_price=300
        )

        self.reservation1 = Reservation.objects.create(
            cust=self.customer,
            apartment=self.apartment2,
            start_date=datetime.now().date() + timedelta(days=25),
            end_date=datetime.now().date() + timedelta(days=27),
            total_price=450
        )

        self.reservation2 = Reservation.objects.create(
            cust=self.customer,
            apartment=self.apartment2,
            start_date=datetime.now().date() + timedelta(days=35),
            end_date=datetime.now().date() + timedelta(days=37),
            total_price=450
        )

        self.reservation3 = Reservation.objects.create(
            cust=self.customer,
            apartment=self.apartment4,
            start_date=datetime.now().date() + timedelta(days=35),
            end_date=datetime.now().date() + timedelta(days=37),
            total_price=150
        )

    def test_customer_menu_no_filters(self):
        # Login como cliente
        self.client.login(username='customer', password='password123')
        response = self.client.get(reverse('customer_menu'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.apartment1.address)
        self.assertContains(response, self.apartment2.address)
        self.assertContains(response, self.apartment4.address)
        self.assertNotContains(response, self.apartment3.address)

    def test_customer_menu_with_price_min(self):
        self.client.login(username='customer', password='password123')
        response = self.client.get(reverse('customer_menu'), {'precio_min': '100'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.apartment1.address)
        self.assertContains(response, self.apartment2.address)
        self.assertNotContains(response, self.apartment4.address)

    def test_customer_menu_with_price_max(self):
        self.client.login(username='customer', password='password123')
        response = self.client.get(reverse('customer_menu'), {'precio_max': '150'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.apartment1.address)
        self.assertContains(response, self.apartment2.address)
        self.assertContains(response, self.apartment4.address)
        self.assertNotContains(response, self.apartment3.address)

    def test_customer_menu_with_guests_filter(self):
        self.client.login(username='customer', password='password123')
        response = self.client.get(reverse('customer_menu'), {'huespedes': '2'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.apartment1.address)
        self.assertNotContains(response, self.apartment2.address)

    def test_customer_menu_with_date_filter(self):
        self.client.login(username='customer', password='password123')
        response = self.client.get(reverse('customer_menu'), {'fecha_inicio': '2024-12-18', 'fecha_fin': '2024-12-20'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.apartment1.address)
        self.assertNotContains(response, self.apartment2.address)

    def test_customer_menu_with_multiple_filters(self):
        self.client.login(username='customer', password='password123')
        response = self.client.get(reverse('customer_menu'), {
            'precio_min': '100',
            'precio_max': '200',
            'huespedes': '2',
            'fecha_inicio': '2024-12-17',
            'fecha_fin': '2024-12-19'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.apartment1.address)
        self.assertNotContains(response, self.apartment2.address)
        self.assertNotContains(response, self.apartment4.address)

    def test_manage_reservations_no_cancel(self):
        self.client.login(username='customer', password='password123')
        response = self.client.get(reverse('manage_reservations'))
        self.assertEqual(response.status_code, 200)
        self.reservation1.refresh_from_db()
        self.assertFalse(self.reservation1.can_cancel)
        self.reservation2.refresh_from_db()
        self.assertTrue(self.reservation2.can_cancel)
        self.reservation3.refresh_from_db()
        self.assertTrue(self.reservation3.can_cancel)

    def test_manage_reservations_with_cancel(self):
        self.reservation1.start_date = datetime.now().date() + timedelta(days=31)  # Más de 30 días
        self.reservation1.save()

        self.client.login(username='customer', password='password123')
        response = self.client.get(reverse('manage_reservations'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.reservation1.can_cancel)
