from django.test import TestCase, Client
from django.urls import reverse
from app.models import CustomUser
from app.forms.CustomUserCreationForm import CustomUserCreationForm
from app.forms.EmailAuthenticationForm import EmailAuthenticationForm
from unittest.mock import patch

class AuthTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_customer = CustomUser.objects.create_user(
            username='customer',
            email='customer@example.com',
            password='password123',
            role='customer'
        )
        self.user_owner = CustomUser.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='password123',
            role='owner'
        )
    
    def test_register_view_valid_form_customer(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'role': 'customer',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/auth/login/')

    def test_register_view_valid_form_owner(self):
        data = {
            'username': 'newowner',
            'email': 'newowner@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'role': 'owner',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/auth/login/')

    def test_register_view_invalid_form(self):
        data = {
            'username': '',
            'email': 'invalidemail',
            'password1': '123',
            'password2': '456',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)  # Re-render form
        self.assertTemplateUsed(response, 'auth/register.html')

    def test_login_view_valid_customer(self):
        data = {
            'email': self.user_customer.email,
            'password': 'password123',
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/customer_menu/')

    def test_login_view_valid_owner(self):
        data = {
            'email': self.user_owner.email,
            'password': 'password123',
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/owner_menu/')

    def test_login_view_invalid_credentials(self):
        data = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword',
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')

    def test_menu_view_customer(self):
        self.client.login(username=self.user_customer.username, password='password123')
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/customer_menu/')

    def test_menu_view_owner(self):
        self.client.login(username=self.user_owner.username, password='password123')
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/owner_menu/')

    def test_edit_profile_view(self):
        self.client.login(username=self.user_customer.username, password='password123')
        data = {
            'username': 'updatedcustomer',
            'email': 'updated@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        }
        response = self.client.post(reverse('edit_profile'), data)
        self.assertEqual(response.status_code, 302)
        self.user_customer.refresh_from_db()
        self.assertEqual(self.user_customer.username, 'updatedcustomer')

    def test_delete_account_view(self):
        self.client.login(username=self.user_customer.username, password='password123')
        response = self.client.post(reverse('delete_account'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CustomUser.objects.filter(username='customer').exists())
