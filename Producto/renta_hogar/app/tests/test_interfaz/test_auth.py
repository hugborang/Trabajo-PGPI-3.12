from django.test import TransactionTestCase, TestCase, LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAuthTests(LiveServerTestCase):
    fixtures = ["populate_data.json"]

    def setUp(self):
        chrome_options = Options()
        # Iniciar el navegador con opciones
        service = Service(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=service, options=chrome_options)
        self.browser.get(self.live_server_url)  # Cambia a URL del servidor de pruebas
                

    def tearDown(self):
        self.browser.quit()

    def test_register(self):

        
        self.browser.get(self.live_server_url)  # Cambia a URL del servidor de pruebas
    

        user_icon = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
        )
        user_icon.click()

        register_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Registrarse"))
        )
        register_button.click()

        self.assertIn("Registrarse", self.browser.page_source)

        username_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_field.send_keys("nuevo_usuario")

        email_field = self.browser.find_element(By.NAME, "email")
        email_field.send_keys("correo@dominio.com")

        password1_field = self.browser.find_element(By.NAME, "password1")
        password1_field.send_keys("contraseña_segura")

        password2_field = self.browser.find_element(By.NAME, "password2")
        password2_field.send_keys("contraseña_segura")

        role_field = self.browser.find_element(By.NAME, "role")
        role_field.send_keys("customer")  

        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
        submit_button.click()
           
        self.assertIn("Iniciar Sesión", self.browser.page_source)  
        
    def test_login(self):
       
        self.browser.get(self.live_server_url)  # Cambia a URL del servidor de pruebas

        user_icon = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
        )
        user_icon.click()

        login_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Iniciar sesión"))
        )
        login_button.click()

        self.assertIn("Iniciar Sesión", self.browser.page_source)

        email_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_field.send_keys("customer1@example.com")

        password_field = self.browser.find_element(By.NAME, "password")
        password_field.send_keys("customer1_password")

        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
        submit_button.click()

        user_icon = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
        )
        user_icon.click()

        logout_button = WebDriverWait(self.browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.user-menu-item.logout-btn"))
    )
        
        self.assertEqual(logout_button.text, "Cerrar sesión")



    def test_edit_profile(self):

        self.browser.get(self.live_server_url)  # Cambia a URL del servidor de pruebas

        user_icon = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
        )
        user_icon.click()

        login_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Iniciar sesión"))
        )
        login_button.click()

        self.assertIn("Iniciar Sesión", self.browser.page_source)

        email_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_field.send_keys("customer1@example.com")

        password_field = self.browser.find_element(By.NAME, "password")
        password_field.send_keys("customer1_password")

        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
        submit_button.click()
        
        user_icon = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
        )
        user_icon.click()

        edit_profile = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.user-menu-item[href='/auth/edit_profile']"))
        )

        edit_profile.click()
        
        self.assertIn("Mis datos", self.browser.page_source)

        username_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_field.clear()
        username_field.send_keys("new_customer")

        email_field = self.browser.find_element(By.NAME, "email")
        email_field.clear()
        email_field.send_keys("new_customer@example.com")

        password_field = self.browser.find_element(By.NAME, "password1")
        password_field.send_keys("new_password123")

        confirm_password_field = self.browser.find_element(By.NAME, "password2")
        confirm_password_field.send_keys("new_password123")

        update_button = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Actualizar']")
        update_button.click()


        user_icon = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
        )
        user_icon.click()

        edit_profile = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.user-menu-item[href='/auth/edit_profile']"))
        )
        edit_profile.click()

        updated_username = self.browser.find_element(By.NAME, "username").get_attribute("value")
        updated_email = self.browser.find_element(By.NAME, "email").get_attribute("value")
        self.assertEqual(updated_username, "new_customer")
        self.assertEqual(updated_email, "new_customer@example.com")



    def test_logout(self):

        self.browser.get(self.live_server_url)  # Cambia a URL del servidor de pruebas

        user_icon = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
        )
        user_icon.click()

        login_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Iniciar sesión"))
        )
        login_button.click()

        self.assertIn("Iniciar Sesión", self.browser.page_source)

        email_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_field.send_keys("customer1@example.com")

        password_field = self.browser.find_element(By.NAME, "password")
        password_field.send_keys("customer1_password")

        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
        submit_button.click()

        user_icon = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
        )
        user_icon.click()

        logout_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.user-menu-item.logout-btn"))
        )
        self.assertEqual(logout_button.text, "Cerrar sesión")
        logout_button.click()

        user_icon = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
        )
        user_icon.click()

        try:
            logout_button = WebDriverWait(self.browser, 2).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "button.user-menu-item.logout-btn"))
            )
            self.fail("El botón de 'Cerrar sesión' no debería estar visible después de hacer clic en el ícono de usuario.")
        except TimeoutException:
            pass



    def test_delete_acount(self):

            self.browser.get(self.live_server_url)  

            user_icon = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
            )
            user_icon.click()

            login_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Iniciar sesión"))
            )
            login_button.click()

            self.assertIn("Iniciar Sesión", self.browser.page_source)

            email_field = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_field.send_keys("customer1@example.com")

            password_field = self.browser.find_element(By.NAME, "password")
            password_field.send_keys("customer1_password")

            submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
            submit_button.click()
            
            user_icon = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
            )
            user_icon.click()

            edit_profile = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.user-menu-item[href='/auth/edit_profile']"))
            )

            edit_profile.click()
            
            self.assertIn("Mis datos", self.browser.page_source)
            
            buttons = self.browser.find_elements(By.CSS_SELECTOR, "button[type='submit']")        
            for button in buttons:
             if button.text.strip() == "Eliminar cuenta":
                button.click()
                break 
            
            # Maneja el cuadro de diálogo de confirmación
            alert = WebDriverWait(self.browser, 10).until(EC.alert_is_present())
            alert.accept()

            
            user_icon = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
            )
            user_icon.click()

            login_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Iniciar sesión"))
            )
            login_button.click()

            self.assertIn("Iniciar Sesión", self.browser.page_source)

            email_field = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_field.send_keys("customer1@example.com")

            password_field = self.browser.find_element(By.NAME, "password")
            password_field.send_keys("customer1_password")

            submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
            submit_button.click()
            
            self.assertIn("Correo electrónico incorrecto", self.browser.page_source)

            

                