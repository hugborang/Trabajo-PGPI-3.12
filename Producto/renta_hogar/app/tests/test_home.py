from django.test import TestCase
from django.urls import reverse
from app.models import Apartment, CustomUser, Availability


class SearchApartmentTests(TestCase):

    def setUp(self):
        # Crear un usuario propietario
        self.owner = CustomUser.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="password123",
            role="owner"
        )

        # Crear apartamentos de prueba
        self.apartment1 = Apartment.objects.create(
            owner=self.owner,
            address="123 Test St",
            guest_count=2,
            description="A small cozy apartment",
            price=50.0,
            is_visible=True
        )
        self.apartment2 = Apartment.objects.create(
            owner=self.owner,
            address="456 Example Ave",
            guest_count=4,
            description="A large apartment for families",
            price=150.0,
            is_visible=True
        )
        self.apartment3 = Apartment.objects.create(
            owner=self.owner,
            address="789 Example Blvd",
            guest_count=6,
            description="Luxury penthouse",
            price=300.0,
            is_visible=True
        )

        # Crear disponibilidades
        Availability.objects.create(
            apartment=self.apartment1,
            start_date="2024-12-20",
            end_date="2024-12-25",
        )
        Availability.objects.create(
            apartment=self.apartment2,
            start_date="2024-12-15",
            end_date="2024-12-22",
        )

    def test_search_no_filters(self):
        response = self.client.get(reverse('home_search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.apartment1.address)
        self.assertContains(response, self.apartment2.address)
        self.assertContains(response, self.apartment3.address)

    def test_filter_by_huespedes(self):
        response = self.client.get(reverse('home_search'), {'huespedes': 4})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.apartment2.address)
        self.assertNotContains(response, self.apartment1.address)
        self.assertNotContains(response, self.apartment3.address)

    def test_filter_by_huespedes_invalid_number(self):
        response = self.client.get(reverse('home_search'), {'huespedes': 'abc'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "El número de huéspedes debe ser un número entero.")
        self.assertContains(response, self.apartment1.address)
        self.assertContains(response, self.apartment2.address)

    def test_filter_by_huespedes_negative_number(self):
        response = self.client.get(reverse('home_search'), {'huespedes': -1})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "El número de huéspedes debe ser mayor a 0.")

    def test_filter_by_price_min(self):
        response = self.client.get(reverse('home_search'), {'precio_min': 100})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.apartment1.address)
        self.assertContains(response, self.apartment2.address)
        self.assertContains(response, self.apartment3.address)

    def test_filter_by_price_min_invalid(self):
        response = self.client.get(reverse('home_search'), {'precio_min': 'invalid'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "El precio mínimo debe ser un número válido.")
        self.assertContains(response, self.apartment1.address)
        self.assertContains(response, self.apartment2.address)

    def test_filter_by_price_max(self):
        response = self.client.get(reverse('home_search'), {'precio_max': 150})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.apartment1.address)
        self.assertContains(response, self.apartment2.address)
        self.assertNotContains(response, self.apartment3.address)

    def test_filter_by_price_max_invalid(self):
        response = self.client.get(reverse('home_search'), {'precio_max': 'invalid'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "El precio máximo debe ser un número válido.")

    def test_filter_by_price_min_greater_than_max(self):
        response = self.client.get(reverse('home_search'), {'precio_min': 200, 'precio_max': 100})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "El precio máximo no puede ser menor al precio mínimo.")

    def test_filter_by_dates(self):
        response = self.client.get(reverse('home_search'), {'fecha_inicio': '2024-12-20', 'fecha_fin': '2024-12-24'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.apartment1.address)
        self.assertNotContains(response, self.apartment2.address)

    def test_filter_by_dates_no_overlap(self):
        response = self.client.get(reverse('home_search'), {'fecha_inicio': '2024-12-10', 'fecha_fin': '2024-12-14'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.apartment1.address)
        self.assertNotContains(response, self.apartment2.address)

    def test_filter_by_dates_invalid(self):
        response = self.client.get(reverse('home_search'), {'fecha_inicio': '2023-02-29', 'fecha_fin': '2023-03-03'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Las fechas deben ser válidas.")

    def test_filter_all_criteria(self):
        response = self.client.get(reverse('home_search'), {
            'precio_min': 100,
            'precio_max': 200,
            'huespedes': 4,
            'fecha_inicio': '2024-12-15',
            'fecha_fin': '2024-12-20',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.apartment2.address)
        self.assertNotContains(response, self.apartment1.address)
        self.assertNotContains(response, self.apartment3.address)
