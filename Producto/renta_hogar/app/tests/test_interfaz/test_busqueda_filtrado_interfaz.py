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

    def test_precio(self):

        self.browser.get(self.live_server_url) 
        self.browser.set_window_size(734, 912)
        self.browser.find_element(By.ID, "price_min").click()
        self.browser.find_element(By.ID, "price_min").send_keys("30")
        self.browser.find_element(By.ID, "price_max").click()
        self.browser.find_element(By.ID, "price_max").send_keys("120")
        self.browser.find_element(By.CSS_SELECTOR, ".btn-buscar").click()

        time.sleep(2)
        # Encuentra el ul que contiene los elementos <a>
        ul_element = self.browser.find_element(By.CSS_SELECTOR, "ul")
        
        # Encuentra todos los elementos <a> dentro del ul
        links = ul_element.find_elements(By.CSS_SELECTOR, "a")
        
        # Verifica que hay exactamente un solo <a>
        self.assertEqual(len(links), 1, f"Se esperaba 1 apartamento, pero se encontraron {len(links)}")

    def test_huespedes(self):

        self.browser.get(self.live_server_url)
        self.browser.set_window_size(734, 912)
        self.browser.find_element(By.ID, "huespedes").click()
        self.browser.find_element(By.ID, "huespedes").send_keys("2")
        self.browser.find_element(By.CSS_SELECTOR, ".btn-buscar").click()

        time.sleep(2)
        # Encuentra el ul que contiene los elementos <a>
        ul_element = self.browser.find_element(By.CSS_SELECTOR, "ul")
        
        # Encuentra todos los elementos <a> dentro del ul
        links = ul_element.find_elements(By.CSS_SELECTOR, "a")
        
        # Verifica que hay exactamente un solo <a>
        self.assertEqual(len(links), 1, f"Se esperaba 1 apartamento, pero se encontraron {len(links)}")
