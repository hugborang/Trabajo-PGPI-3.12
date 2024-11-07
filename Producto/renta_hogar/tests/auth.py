from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from app.forms.CustomUserCreationForm import CustomUserCreationForm

class AuthViewTests(TestCase):
    def setUp(self):
        # Crear un cliente para realizar solicitudes
        self.client = Client()
        
        # Crear un usuario para las pruebas de inicio y cierre de sesión
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword123',
            role='customer'  # Cambia el campo role si tu modelo de usuario es diferente
        )

    def test_register_view_get(self):
        # Prueba para la vista de registro con el método GET
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')

    def test_register_view_post(self):
        # Prueba para el registro de un nuevo usuario con el método POST
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'role': 'customer'  # Asegúrate de incluir todos los campos necesarios
        })
        self.assertEqual(response.status_code, 302)  # Redirige después de registro
        self.assertEqual(response.url, '/auth/login/')  # Verifica la URL de redirección

    def test_user_login_view_get(self):
        # Prueba para la vista de inicio de sesión con el método GET
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')

    def test_user_login_view_post_customer(self):
        # Prueba para el inicio de sesión de un usuario con rol "customer"
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/customer_menu')  # Redirige al menú de cliente

    def test_user_login_view_post_owner(self):
        # Cambia el rol del usuario a "owner" y prueba la redirección
        self.user.role = 'owner'
        self.user.save()
        
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/owner_menu')  # Redirige al menú de propietario

    def test_user_logout_view(self):
        # Prueba para el cierre de sesión de un usuario
        self.client.login(username='testuser', password='testpassword123')  # Inicia sesión
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))  # Redirige a la página de inicio
