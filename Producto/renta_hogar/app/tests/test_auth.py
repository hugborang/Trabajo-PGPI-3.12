from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from app.forms.CustomUserCreationForm import CustomUserCreationForm

class AuthViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword123',
            role='customer'  
        )

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')

    def test_register_view_post(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'surnames': 'New User',
            'email': 'email@gmail.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'role': 'customer'  
        })
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(response.url, '/auth/login/')  

    def test_user_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')

    def test_user_login_view_post_customer(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/customer_menu')  

    def test_user_login_view_post_owner(self):
        self.user.role = 'owner'
        self.user.save()
        
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/owner_menu') 

    def test_user_logout_view(self):
        self.client.login(username='testuser', password='testpassword123')  
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))  
