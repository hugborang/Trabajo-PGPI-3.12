from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from app.forms.CustomUserCreationForm import CustomUserCreationForm
from django.contrib.messages import get_messages

class AuthViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword123',
            role='customer'  
        )

    # Tests de la vista de register
    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')

    def test_register_view_post_customer(self):
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
        
    def test_register_view_post_owner(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'surnames': 'New User',
            'email': 'email@gmail.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'role': 'owner'  
        })
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(response.url, '/auth/login/')  


    # Tests de la vista de login
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

    #Tests de la vista edit_profile
    
    def test_get_edit_profile(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/edit_profile.html')
        self.assertIn('form', response.context)
        self.assertIn('password_form', response.context)


    

    # Tests de la vista de logout
    def test_user_logout_view(self):
        self.client.login(username='testuser', password='testpassword123')  
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))  

    # Tests de la vista de delete_account
    def test_user_delete_account_view(self):
        self.client.login(username='testuser', password='testpassword123')  
        response = self.client.get(reverse('delete_account'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))