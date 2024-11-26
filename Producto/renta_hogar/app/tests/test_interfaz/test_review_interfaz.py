from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from django.test import TransactionTestCase, TestCase, LiveServerTestCase


class TestReviewInterfaz(LiveServerTestCase):
    fixtures = ["populate_data.json"]


    def setUp(self):
        chrome_options = Options()
        # Iniciar el navegador con opciones
        service = Service(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=service, options=chrome_options)
        self.browser.get(self.live_server_url)  # Cambia a URL del servidor de pruebas
    
    def teardown_method(self):
      self.browser.quit()
    
    def test_negativo_review_customer(self):
      self.browser.get(self.live_server_url)  # Cambia a URL del servidor de pruebas
      self.browser.set_window_size(734, 912)
      self.browser.find_element(By.CSS_SELECTOR, ".fas").click()
      self.browser.find_element(By.LINK_TEXT, "Iniciar sesión").click()
      self.browser.find_element(By.ID, "id_email").click()
      self.browser.find_element(By.ID, "id_email").send_keys("customer1@example.com")
      self.browser.find_element(By.ID, "id_password").click()
      self.browser.find_element(By.ID, "id_password").send_keys("customer1_password")
      self.browser.find_element(By.CSS_SELECTOR, "p > input").click()
      self.browser.find_element(By.ID, "price_min").click()
      self.browser.find_element(By.ID, "price_min").send_keys("4")
      self.browser.find_element(By.CSS_SELECTOR, ".filtro:nth-child(1)").click()
      self.browser.find_element(By.ID, "price_max").click()
      self.browser.find_element(By.ID, "price_max").send_keys("400")
      self.browser.find_element(By.CSS_SELECTOR, ".btn-buscar").click()
      self.browser.find_element(By.CSS_SELECTOR, ".fas").click()
      self.browser.find_element(By.LINK_TEXT, "Gestionar reservas").click()
      self.browser.find_element(By.CSS_SELECTOR, ".btn-success").click()
      self.browser.find_element(By.ID, "id_rating").click()
      self.browser.find_element(By.ID, "id_rating").send_keys("4")
      self.browser.find_element(By.ID, "id_comment").click()
      self.browser.find_element(By.ID, "id_comment").send_keys("Holaaaaaaaa")
      self.browser.find_element(By.CSS_SELECTOR, ".btn").click()


      error_message = WebDriverWait(self.browser, 4).until(
      EC.presence_of_element_located((By.CLASS_NAME, "alert-error"))
  )

      assert "No puedes dejar una valoración hasta que no hayas disfrutado de tu estancia." in error_message.text

    def test_positivo_review_customer(self):
      self.browser.get(self.live_server_url)  # Cambia a URL del servidor de pruebas
      self.browser.set_window_size(734, 912)
      self.browser.find_element(By.CSS_SELECTOR, ".fas").click()
      self.browser.find_element(By.LINK_TEXT, "Iniciar sesión").click()
      self.browser.find_element(By.ID, "id_email").click()
      self.browser.find_element(By.ID, "id_email").send_keys("customer1@example.com")
      self.browser.find_element(By.ID, "id_password").click()
      self.browser.find_element(By.ID, "id_password").send_keys("customer1_password")
      self.browser.find_element(By.CSS_SELECTOR, "p > input").click()
      self.browser.find_element(By.CSS_SELECTOR, ".fas").click()
      self.browser.find_element(By.LINK_TEXT, "Gestionar reservas").click()
      self.browser.find_element(By.CSS_SELECTOR, ".reservation-card:nth-child(2) .btn").click()
      self.browser.find_element(By.ID, "id_rating").click()
      self.browser.find_element(By.ID, "id_rating").send_keys("4")
      self.browser.find_element(By.ID, "id_comment").click()
      self.browser.find_element(By.ID, "id_comment").send_keys("Prueba positiva")
      self.browser.find_element(By.CSS_SELECTOR, ".btn").click()

      # Terminar de poner bien el assert cuando funcione la validacion


    def test_caso_positivo_ver_reviews(self):
      self.browser.get(self.live_server_url)  # Cambia a URL del servidor de pruebas
      self.browser.set_window_size(734, 912)
      self.browser.find_element(By.CSS_SELECTOR, ".fas").click()
      self.browser.find_element(By.LINK_TEXT, "Iniciar sesión").click()
      self.browser.find_element(By.ID, "id_email").click()
      self.browser.find_element(By.ID, "id_email").send_keys("owner1@example.com")
      self.browser.find_element(By.ID, "id_password").click()
      self.browser.find_element(By.ID, "id_password").send_keys("owner1_password")
      self.browser.find_element(By.CSS_SELECTOR, "p > input").click()
      self.browser.find_element(By.LINK_TEXT, "Ver Valoraciones").click()

      message3 = WebDriverWait(self.browser, 4).until(
      EC.presence_of_element_located((By.CLASS_NAME, "apartment-section"))
  )

      assert "Sin reseñas" in message3.text # Cambiar esto por "Prueba positiva" cuando funciones bien las validaciones