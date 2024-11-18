from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from app.models import Apartment, ApartmentPhoto
from PIL import Image
import io

User = get_user_model()

class ApartmentManagementTests(TestCase):
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
            address="123 Example St",
            guest_count=2,
            description="Apartamento de prueba",
            is_visible=True,
            price=100.00  # Precio inicial
        )

        photos = [
            self.create_test_image(name=f"photo{i}.jpg") for i in range(3)
        ]

        for photo in photos:
            ApartmentPhoto.objects.create(apartment=self.apartment, photo=photo)

    @staticmethod
    def create_test_image(name="test.jpg", size=(100, 100), color=(255, 0, 0)):
        file = io.BytesIO()
        image = Image.new("RGB", size, color)
        image.save(file, format="JPEG")
        file.seek(0)
        return SimpleUploadedFile(name, file.read(), content_type="image/jpeg")

    ### Pruebas de añadir apartamento ###
    def test_add_apartment_as_owner(self):
        self.client.login(username="owner1", password="password123")
        photo1 = self.create_test_image(name="photo1.jpg")
        response = self.client.post(reverse("add_apartment"), {
            'address': "456 New St",
            'guest_count': 2,
            'description': "Nuevo apartamento",
            'is_visible': True,
            'price': 150.00,
            'photos': [photo1],
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Apartment.objects.filter(address="456 New St", price=150.00).exists())

    def test_add_apartment_as_customer(self):
        self.client.login(username="customer1", password="password123")
        photo1 = self.create_test_image(name="photo1.jpg")
        response = self.client.post(reverse("add_apartment"), {
            'address': "789 New St",
            'guest_count': 2,
            'description': "Intento de añadir apartamento",
            'is_visible': True,
            'price': 200.00,
            'photos': [photo1],
        }, follow=True)

        self.assertEqual(response.status_code, 403)
        self.assertIn("No tienes permiso para añadir apartamentos", response.content.decode())
        self.assertFalse(Apartment.objects.filter(address="789 New St").exists())

    def test_add_apartment_with_invalid_guest_count(self):
        self.client.login(username="owner1", password="password123")
        photo1 = self.create_test_image(name="photo1.jpg")
        response = self.client.post(reverse("add_apartment"), {
            'address': "789 New St",
            'guest_count': 0,
            'description': "Intento de añadir apartamento",
            'is_visible': True,
            'price': 100.00,
            'photos': [photo1],
        })

        self.assertContains(response, "La capacidad de huéspedes debe ser mayor que 0")
        self.assertFalse(Apartment.objects.filter(address="789 New St").exists())

    def test_add_apartment_with_negative_price(self):
        self.client.login(username="owner1", password="password123")
        photo1 = self.create_test_image(name="photo1.jpg")
        response = self.client.post(reverse("add_apartment"), {
            'address': "456 Negative Price St",
            'guest_count': 2,
            'description': "Apartamento con precio negativo",
            'is_visible': True,
            'price': -50.00,
            'photos': [photo1],
        })

        self.assertContains(response, "El precio no puede ser negativo")
        self.assertFalse(Apartment.objects.filter(address="456 Negative Price St").exists())

    def test_add_apartment_with_no_photos(self):
        self.client.login(username="owner1", password="password123")
        response = self.client.post(reverse("add_apartment"), {
            'address': "789 New St",
            'guest_count': 2,
            'description': "Intento de añadir apartamento",
            'is_visible': True,
            'price': 150.00,
        })

        self.assertContains(response, "Debes subir al menos una foto del apartamento")
        self.assertFalse(Apartment.objects.filter(address="789 New St").exists())

    def test_add_apartment_with_invalid_photos(self):
        self.client.login(username="owner1", password="password123")
        photo = SimpleUploadedFile("photo.txt", b"file_content", content_type="text/plain")
        response = self.client.post(reverse("add_apartment"), {
            'address': "987 Photo St",
            'guest_count': 3,
            'description': "Apartamento con fotos",
            'is_visible': True,
            'price': 200.00,
            'photos': [photo],
        })

        self.assertContains(response, "Solo se permiten archivos de imagen con las extensiones: .jpg, .jpeg, .png, .gif")
        self.assertFalse(Apartment.objects.filter(address="987 Photo St").exists())

    ### Pruebas de eliminar apartamento ###
    def test_delete_apartment_as_owner(self):
        self.client.login(username="owner1", password="password123")
        response = self.client.post(reverse("delete_apartment", args=[self.apartment.id]), follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Apartment.objects.filter(id=self.apartment.id).exists())

    def test_owner_cannot_delete_another_owners_apartment(self):
        self.client.login(username="owner2", password="password123")
        response = self.client.post(reverse("delete_apartment", args=[self.apartment.id]), follow=True)
        
        self.assertEqual(response.status_code, 403)
        self.assertIn("No tienes permiso para eliminar este apartamento", response.content.decode())
        self.assertTrue(Apartment.objects.filter(id=self.apartment.id).exists())

    def test_delete_apartment_as_customer(self):
        self.client.login(username="customer1", password="password123")
        response = self.client.post(reverse("delete_apartment", args=[self.apartment.id]), follow=True)

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Apartment.objects.filter(id=self.apartment.id).exists())

    ### Pruebas de editar apartamento ###
    def test_edit_apartment_as_owner(self):
        self.client.login(username="owner1", password="password123")
        photo4 = self.create_test_image(name="photo4.jpg")
        existing_photos = [photo.id for photo in self.apartment.photos.all()]
        response = self.client.post(reverse("edit_apartment", args=[self.apartment.id]), {
            'address': "123 Updated St",
            'guest_count': 4,
            'description': "Apartamento actualizado",
            'is_visible': True,
            'price': 200.00,
            'photos': [photo4],
            'existing_photos': existing_photos,
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.apartment.refresh_from_db()
        self.assertEqual(self.apartment.address, "123 Updated St")
        self.assertEqual(self.apartment.price, 200.00)
        self.assertEqual(self.apartment.photos.count(), 4)

    def test_edit_nonexistent_apartment(self):
        self.client.login(username="owner1", password="password123")
        photo = self.create_test_image(name="photo.jpg")
        response = self.client.post(reverse("edit_apartment", args=[100]), {
            'address': "123 Updated St",
            'guest_count': 4,
            'description': "Apartamento actualizado",
            'is_visible': True,
            'price': 200.00,
            'photos': [photo],
        })

        self.assertEqual(response.status_code, 404)

    def test_owner_cannot_edit_another_owners_apartment(self):
        self.client.login(username="owner2", password="password123")
        photo4 = self.create_test_image(name="photo4.jpg")
        existing_photos = [photo.id for photo in self.apartment.photos.all()]
        response = self.client.post(reverse("edit_apartment", args=[self.apartment.id]), {
            'address': "Nuevo domicilio",
            'guest_count': 4,
            'description': "Intento de edición de otro propietario",
            'is_visible': True,
            'price': 200.00,
            'photos': [photo4],
            'existing_photos': existing_photos,
        }, follow=True)

        self.assertEqual(response.status_code, 403)
        self.assertIn("No tienes permiso para editar este apartamento", response.content.decode())
        apartment = Apartment.objects.get(id=self.apartment.id)
        self.assertNotEqual(apartment.address, "Nuevo domicilio")
        self.assertNotEqual(apartment.guest_count, 4)
        self.assertNotEqual(apartment.description, "Intento de edición de otro propietario")

    def test_edit_apartment_as_customer(self):
        self.client.login(username="customer1", password="password123")
        photo4 = self.create_test_image(name="photo4.jpg")
        existing_photos = [photo.id for photo in self.apartment.photos.all()]
        response = self.client.post(reverse("edit_apartment", args=[self.apartment.id]), {
            'address': "789 Fail St",
            'guest_count': 2,
            'description': "Intento de editar",
            'is_visible': False,
            'price': 150.00,
            'photos': [photo4],
            'existing_photos': existing_photos,
        }, follow=True)

        self.assertEqual(response.status_code, 403)
        self.apartment.refresh_from_db()
        self.assertNotEqual(self.apartment.address, "789 Fail St")

    def test_edit_apartment_with_invalid_guest_count(self):
        self.client.login(username="owner1", password="password123")
        photo4 = self.create_test_image(name="photo4.jpg")
        existing_photos = [photo.id for photo in self.apartment.photos.all()]
        response = self.client.post(reverse("edit_apartment", args=[self.apartment.id]), {
            'address': "123 Updated St",
            'guest_count': 0,
            'description': "Apartamento actualizado",
            'is_visible': True,
            'price': 200.00,
            'photos': [photo4],
            'existing_photos': existing_photos,
        })

        self.assertContains(response, "La capacidad de huéspedes debe ser mayor que 0")
        self.apartment.refresh_from_db()
        self.assertNotEqual(self.apartment.address, "123 Updated St")

    def test_edit_apartment_with_negative_price(self):
        self.client.login(username="owner1", password="password123")
        photo4 = self.create_test_image(name="photo4.jpg")
        existing_photos = [photo.id for photo in self.apartment.photos.all()]
        response = self.client.post(reverse("edit_apartment", args=[self.apartment.id]), {
            'address': "123 Updated St",
            'guest_count': 4,
            'description': "Intento de editar con precio negativo",
            'is_visible': True,
            'price': -100.00,  # Precio negativo
            'photos': [photo4],
            'existing_photos': existing_photos,
        })

        self.assertContains(response, "El precio no puede ser negativo")
        self.apartment.refresh_from_db()
        self.assertNotEqual(self.apartment.price, -100.00)

    def test_edit_apartment_removing_all_photos(self):
        self.client.login(username="owner1", password="password123")
        response = self.client.post(reverse("edit_apartment", args=[self.apartment.id]), {
            'address': "456 Updated St",
            'guest_count': 3,
            'description': "Intento de eliminar todas las fotos",
            'is_visible': True,
            'existing_photos': [],  # No se selecciona ninguna foto existente
        })

        self.assertContains(response, "El apartamento debe tener al menos una foto.")
        self.apartment.refresh_from_db()
        self.assertEqual(self.apartment.photos.count(), 3)  # Las fotos no se eliminaron

    def test_edit_apartment_with_invalid_photos(self):
        self.client.login(username="owner1", password="password123")
        photo = SimpleUploadedFile("photo.txt", b"file_content", content_type="text/plain")
        existing_photos = [photo.id for photo in self.apartment.photos.all()]
        response = self.client.post(reverse("edit_apartment", args=[self.apartment.id]), {
            'address': "456 Updated St",
            'guest_count': 2,
            'description': "Intento de editar con foto inválida",
            'is_visible': True,
            'photos': [photo],
            'existing_photos': existing_photos,
        })

        self.assertContains(response, "Solo se permiten archivos de imagen con las extensiones: .jpg, .jpeg, .png, .gif")
        self.apartment.refresh_from_db()
        self.assertNotEqual(self.apartment.address, "456 Updated St")

    def test_edit_apartment_with_too_many_photos(self):
        self.client.login(username="owner1", password="password123")
        photos = [
            self.create_test_image(name=f"photo{i}.jpg") for i in range(3)
        ]
        existing_photos = [photo.id for photo in self.apartment.photos.all()]
        response = self.client.post(reverse("edit_apartment", args=[self.apartment.id]), {
            'address': "456 Updated St",
            'guest_count': 2,
            'description': "Intento de editar con demasiadas fotos",
            'is_visible': True,
            'price': 150.00,
            'photos': photos,
            'existing_photos': existing_photos,
        })

        self.assertContains(response, "Solo puedes subir hasta 5 fotos del apartamento")
        self.apartment.refresh_from_db()
        self.assertNotEqual(self.apartment.address, "456 Updated St")
