import time
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
        
    def test_crear_reserva(self):
        
        self.browser.get(self.live_server_url) 
        self.browser.set_window_size(974, 1040)
        self.browser.find_element(By.CSS_SELECTOR, ".fas").click()
        self.browser.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.browser.find_element(By.ID, "id_email").click()
        self.browser.find_element(By.ID, "id_email").send_keys("customer1@example.com")
        self.browser.find_element(By.ID, "id_password").click()
        self.browser.find_element(By.ID, "id_password").send_keys("customer1_password")
        self.browser.find_element(By.CSS_SELECTOR, "p > input").click()
        self.browser.find_element(By.CSS_SELECTOR, "a:nth-child(1) .apartment-photo").click()
        date_range = "2024-12-22 a 2024-12-27"
        self.browser.execute_script(
            'document.getElementById("fecha_rango").value = arguments[0];', date_range
        )
        self.browser.find_element(By.ID, "openModalButton").click()

        modal = self.browser.find_element(By.CLASS_NAME, "modal-content")
        self.assertTrue(modal.is_displayed(), "El modal no se mostró correctamente.")

        # Comprobar los elementos clave dentro del modal

        modal_title = self.browser.find_element(By.CSS_SELECTOR, ".modal-content h2").text
        self.assertEqual(modal_title, "Confirmar Reserva", "El modal no contiene el título esperado.")
       
       
    def test_cancelar_reserva(self):
        
        self.browser.get(self.live_server_url) 
        self.browser.set_window_size(974, 1040)
        self.browser.find_element(By.CSS_SELECTOR, ".fas").click()
        self.browser.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.browser.find_element(By.ID, "id_email").click()
        self.browser.find_element(By.ID, "id_email").send_keys("customer1@example.com")
        self.browser.find_element(By.ID, "id_password").click()
        self.browser.find_element(By.ID, "id_password").send_keys("customer1_password")
        self.browser.find_element(By.CSS_SELECTOR, "p > input").click()
        self.browser.find_element(By.CSS_SELECTOR, ".user-menu-icon").click()
        self.browser.find_element(By.LINK_TEXT, "Gestionar reservas").click()
        self.browser.find_element(By.CSS_SELECTOR, ".btn-danger").click()
        self.browser.find_element(By.CSS_SELECTOR, ".btn-primary").click()

        time.sleep(3)  
        reservations = self.browser.find_elements(By.CSS_SELECTOR, ".reservation-card")
        self.assertEqual(len(reservations), 3, f"Se esperaban 3 reservas, pero se encontraron {len(reservations)}")
        
    def test_owner_ver(self):
        
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(974, 1040)
        self.browser.find_element(By.CSS_SELECTOR, ".fas").click()
        self.browser.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.browser.find_element(By.ID, "id_email").click()
        self.browser.find_element(By.ID, "id_email").send_keys("owner1@example.com")
        self.browser.find_element(By.ID, "id_password").click()
        self.browser.find_element(By.ID, "id_password").send_keys("owner1_password")
        self.browser.find_element(By.CSS_SELECTOR, "p > input").click()
        self.browser.find_element(By.CSS_SELECTOR, ".user-menu-icon").click()
        self.browser.find_element(By.LINK_TEXT, "Gestionar reservas").click()
        
        time.sleep(3)  
        reservations = self.browser.find_elements(By.CSS_SELECTOR, ".reservation-card")
        self.assertEqual(len(reservations), 3, f"Se esperaban 3 reservas, pero se encontraron {len(reservations)}")