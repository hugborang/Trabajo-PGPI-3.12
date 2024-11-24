from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestUserRegistration(TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")  # Añadir opción si se necesita

        driver_path = ChromeDriverManager().install()
        service = Service(executable_path=driver_path)
        
        self.browser = webdriver.Chrome(service=service, options=chrome_options)
        self.browser.get("http://localhost:8000")  # URL de tu página

    def tearDown(self):
        self.browser.quit()

    def test_click_register(self):
        # Navegar a la página principal
        self.browser.get("http://localhost:8000")

        # Esperar y hacer clic en el icono de usuario
        user_icon = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
        )
        user_icon.click()

        # Esperar y hacer clic en el enlace "Registrarse"
        register_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Registrarse"))
        )
        register_button.click()

        # Verificar que estamos en la página de registro
        self.assertIn("Registrarse", self.browser.page_source)

        # Completar el formulario de registro
        # Esperar a que el campo de nombre de usuario esté presente y rellenarlo
        username_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_field.send_keys("nuevo_usuario")

        # Esperar a que el campo de correo electrónico esté presente y rellenarlo
        email_field = self.browser.find_element(By.NAME, "email")
        email_field.send_keys("correo@dominio.com")

        # Esperar a que el campo de contraseña esté presente y rellenarlo
        password1_field = self.browser.find_element(By.NAME, "password1")
        password1_field.send_keys("contraseña_segura")

        # Esperar a que el campo de repetir la contraseña esté presente y rellenarlo
        password2_field = self.browser.find_element(By.NAME, "password2")
        password2_field.send_keys("contraseña_segura")

        # Esperar a que el campo de rol esté presente y seleccionarlo (Inquilino por defecto)
        role_field = self.browser.find_element(By.NAME, "role")
        role_field.send_keys("customer")  # O "owner" dependiendo del rol deseado

        # Hacer clic en el botón de registro
        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
        submit_button.click()

        # Verificar si el registro fue exitoso
        # Aquí puedes añadir más verificaciones según lo que esperes después del registro
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".welcome-message"))  # O algún otro elemento que indique éxito
        )
        
        # Verificar que el usuario está registrado y redirigido a la página de inicio o la página de bienvenida
        self.assertIn("Bienvenido", self.browser.page_source)  # Ajusta esto según lo que muestra tu aplicación
