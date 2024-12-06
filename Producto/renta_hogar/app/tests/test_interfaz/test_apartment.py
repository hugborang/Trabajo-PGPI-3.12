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
import os

User = get_user_model()


class UserAuthTests(LiveServerTestCase):
    fixtures = ["populate_data.json"]

    def setUp(self):
        chrome_options = Options()
        service = Service(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=service, options=chrome_options)
        self.browser.get(self.live_server_url)  
                

    def tearDown(self):
        self.browser.quit()
    def test_createApartment(self):
        self.browser.get(self.live_server_url)

       
        user_icon = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
        )
        user_icon.click()

        login_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Iniciar sesión"))
        )
        login_button.click()

        email_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_field.send_keys("owner1@example.com")

        password_field = self.browser.find_element(By.NAME, "password")
        password_field.send_keys("owner1_password")

        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
        submit_button.click()

        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        
       
        add_apartment_button = WebDriverWait(self.browser, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.add-property-btn[href='/add_apartment/']"))
        )
        add_apartment_button.click()

        
        self.assertIn("Añadir apartamento", self.browser.page_source)

       
        address_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "address"))
        )
        address_field.send_keys("123 New Street")

        guests_field = self.browser.find_element(By.NAME, "guest_count")
        guests_field.send_keys("4")

        price_field = self.browser.find_element(By.NAME, "price")
        price_field.send_keys("120.00")

        description_field = self.browser.find_element(By.NAME, "description")
        description_field.send_keys("Apartamento moderno y bien ubicado.")

        photo_upload = self.browser.find_element(By.NAME, "photos")

        photo_path = os.path.abspath("media/apartments/test/001beach_apartment.jpeg")
        photo_upload.send_keys(photo_path)
        buttons = self.browser.find_elements(By.CSS_SELECTOR, "button[type='submit']")
        for button in buttons:
            if button.text.strip() == "Guardar Apartamento":
                button.click()
                break 

        self.assertIn("/owner_menu/", self.browser.current_url)
        self.assertIn("123 New Street",self.browser.page_source)
        self.assertIn("4 huéspedes", self.browser.page_source)
        self.assertIn("120,00 €", self.browser.page_source)

    def test_createApartment_largeAddress(self):
        self.browser.get(self.live_server_url)

       
        user_icon = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
        )
        user_icon.click()

        login_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Iniciar sesión"))
        )
        login_button.click()

        email_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_field.send_keys("owner1@example.com")

        password_field = self.browser.find_element(By.NAME, "password")
        password_field.send_keys("owner1_password")

        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
        submit_button.click()

        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        
       
        add_apartment_button = WebDriverWait(self.browser, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.add-property-btn[href='/add_apartment/']"))
        )
        add_apartment_button.click()

        
        self.assertIn("Añadir apartamento", self.browser.page_source)

       
        address_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "address"))
        )
        address_field.send_keys("adreeessssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss234")

        guests_field = self.browser.find_element(By.NAME, "guest_count")
        guests_field.send_keys("0")

        price_field = self.browser.find_element(By.NAME, "price")
        price_field.send_keys("120.00")

        description_field = self.browser.find_element(By.NAME, "description")
        description_field.send_keys("Apartamento moderno y bien ubicado.")

        photo_upload = self.browser.find_element(By.NAME, "photos")

        photo_path = os.path.abspath("media/apartments/test/001beach_apartment.jpeg")
        photo_upload.send_keys(photo_path)
        buttons = self.browser.find_elements(By.CSS_SELECTOR, "button[type='submit']")
        for button in buttons:
            if button.text.strip() == "Guardar Apartamento":
                button.click()
                break 

        self.assertIn("/add_apartment/", self.browser.current_url)

    def test_createApartment_GuestCount_Zero(self):
        self.browser.get(self.live_server_url)

        user_icon = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
        )
        user_icon.click()

        login_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Iniciar sesión"))
        )
        login_button.click()

        email_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_field.send_keys("owner1@example.com")

        password_field = self.browser.find_element(By.NAME, "password")
        password_field.send_keys("owner1_password")

        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
        submit_button.click()

        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

        add_apartment_button = WebDriverWait(self.browser, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.add-property-btn[href='/add_apartment/']"))
        )
        add_apartment_button.click()

        self.assertIn("Añadir apartamento", self.browser.page_source)

        address_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "address"))
        )
        address_field.send_keys("123 New Street")

        guests_field = self.browser.find_element(By.NAME, "guest_count")
        guests_field.send_keys("0")

        price_field = self.browser.find_element(By.NAME, "price")
        price_field.send_keys("120.00")

        description_field = self.browser.find_element(By.NAME, "description")
        description_field.send_keys("Apartamento moderno y bien ubicado.")

        photo_upload = self.browser.find_element(By.NAME, "photos")

        photo_path = os.path.abspath("media/apartments/test/001beach_apartment.jpeg")
        photo_upload.send_keys(photo_path)

        buttons = self.browser.find_elements(By.CSS_SELECTOR, "button[type='submit']")
        for button in buttons:
            if button.text.strip() == "Guardar Apartamento":
                button.click()
                break

        self.assertIn("/add_apartment/", self.browser.current_url)

    def test_createApartment_GuestCount_31(self):
        self.browser.get(self.live_server_url)

        user_icon = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
        )
        user_icon.click()

        login_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Iniciar sesión"))
        )
        login_button.click()

        email_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_field.send_keys("owner1@example.com")

        password_field = self.browser.find_element(By.NAME, "password")
        password_field.send_keys("owner1_password")

        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
        submit_button.click()

        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

        add_apartment_button = WebDriverWait(self.browser, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.add-property-btn[href='/add_apartment/']"))
        )
        add_apartment_button.click()

        self.assertIn("Añadir apartamento", self.browser.page_source)

        address_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "address"))
        )
        address_field.send_keys("123 New Street")

        guests_field = self.browser.find_element(By.NAME, "guest_count")
        guests_field.send_keys("31")

        price_field = self.browser.find_element(By.NAME, "price")
        price_field.send_keys("120.00")

        description_field = self.browser.find_element(By.NAME, "description")
        description_field.send_keys("Apartamento moderno y bien ubicado.")

        photo_upload = self.browser.find_element(By.NAME, "photos")

        photo_path = os.path.abspath("media/apartments/test/001beach_apartment.jpeg")
        photo_upload.send_keys(photo_path)

        buttons = self.browser.find_elements(By.CSS_SELECTOR, "button[type='submit']")
        for button in buttons:
            if button.text.strip() == "Guardar Apartamento":
                button.click()
                break

        self.assertIn("/add_apartment/", self.browser.current_url)

    def test_createApartment_Price_Zero(self):
        self.browser.get(self.live_server_url)

        user_icon = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
        )
        user_icon.click()

        login_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Iniciar sesión"))
        )
        login_button.click()

        email_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_field.send_keys("owner1@example.com")

        password_field = self.browser.find_element(By.NAME, "password")
        password_field.send_keys("owner1_password")

        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
        submit_button.click()

        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

        add_apartment_button = WebDriverWait(self.browser, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.add-property-btn[href='/add_apartment/']"))
        )
        add_apartment_button.click()

        self.assertIn("Añadir apartamento", self.browser.page_source)

        address_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "address"))
        )
        address_field.send_keys("123 New Street")

        guests_field = self.browser.find_element(By.NAME, "guest_count")
        guests_field.send_keys("4")

        price_field = self.browser.find_element(By.NAME, "price")
        price_field.send_keys("0")

        description_field = self.browser.find_element(By.NAME, "description")
        description_field.send_keys("Apartamento moderno y bien ubicado.")

        photo_upload = self.browser.find_element(By.NAME, "photos")

        photo_path = os.path.abspath("media/apartments/test/001beach_apartment.jpeg")
        photo_upload.send_keys(photo_path)

        buttons = self.browser.find_elements(By.CSS_SELECTOR, "button[type='submit']")
        for button in buttons:
            if button.text.strip() == "Guardar Apartamento":
                button.click()
                break

        self.assertIn("/add_apartment/", self.browser.current_url)

    def test_createApartment_Price_MinusOne(self):
        self.browser.get(self.live_server_url)

        user_icon = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
        )
        user_icon.click()

        login_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Iniciar sesión"))
        )
        login_button.click()

        email_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_field.send_keys("owner1@example.com")

        password_field = self.browser.find_element(By.NAME, "password")
        password_field.send_keys("owner1_password")

        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
        submit_button.click()

        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

        add_apartment_button = WebDriverWait(self.browser, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.add-property-btn[href='/add_apartment/']"))
        )
        add_apartment_button.click()

        self.assertIn("Añadir apartamento", self.browser.page_source)

        address_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "address"))
        )
        address_field.send_keys("123 New Street")

        guests_field = self.browser.find_element(By.NAME, "guest_count")
        guests_field.send_keys("4")

        price_field = self.browser.find_element(By.NAME, "price")
        price_field.send_keys("-1")

        description_field = self.browser.find_element(By.NAME, "description")
        description_field.send_keys("Apartamento moderno y bien ubicado.")

        photo_upload = self.browser.find_element(By.NAME, "photos")

        photo_path = os.path.abspath("media/apartments/test/001beach_apartment.jpeg")
        photo_upload.send_keys(photo_path)

        buttons = self.browser.find_elements(By.CSS_SELECTOR, "button[type='submit']")
        for button in buttons:
            if button.text.strip() == "Guardar Apartamento":
                button.click()
                break

        self.assertIn("/add_apartment/", self.browser.current_url)

    def test_createApartment_Price_Eleven_Digits(self):
        self.browser.get(self.live_server_url)

        user_icon = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
        )
        user_icon.click()

        login_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Iniciar sesión"))
        )
        login_button.click()

        email_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_field.send_keys("owner1@example.com")

        password_field = self.browser.find_element(By.NAME, "password")
        password_field.send_keys("owner1_password")

        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
        submit_button.click()

        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

        add_apartment_button = WebDriverWait(self.browser, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.add-property-btn[href='/add_apartment/']"))
        )
        add_apartment_button.click()

        self.assertIn("Añadir apartamento", self.browser.page_source)

        address_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "address"))
        )
        address_field.send_keys("123 New Street")

        guests_field = self.browser.find_element(By.NAME, "guest_count")
        guests_field.send_keys("4")

        price_field = self.browser.find_element(By.NAME, "price")
        price_field.send_keys("100000000000")

        description_field = self.browser.find_element(By.NAME, "description")
        description_field.send_keys("Apartamento moderno y bien ubicado.")

        photo_upload = self.browser.find_element(By.NAME, "photos")

        photo_path = os.path.abspath("media/apartments/test/001beach_apartment.jpeg")
        photo_upload.send_keys(photo_path)

        buttons = self.browser.find_elements(By.CSS_SELECTOR, "button[type='submit']")
        for button in buttons:
            if button.text.strip() == "Guardar Apartamento":
                button.click()
                break

        self.assertIn("/add_apartment/", self.browser.current_url)


    def test_createApartment_With_Out_Photo(self):
        self.browser.get(self.live_server_url)

        user_icon = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
        )
        user_icon.click()

        login_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Iniciar sesión"))
        )
        login_button.click()

        email_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_field.send_keys("owner1@example.com")

        password_field = self.browser.find_element(By.NAME, "password")
        password_field.send_keys("owner1_password")

        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
        submit_button.click()

        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

        add_apartment_button = WebDriverWait(self.browser, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.add-property-btn[href='/add_apartment/']"))
        )
        add_apartment_button.click()

        self.assertIn("Añadir apartamento", self.browser.page_source)

        address_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "address"))
        )
        address_field.send_keys("123 New Street")

        guests_field = self.browser.find_element(By.NAME, "guest_count")
        guests_field.send_keys("4")

        price_field = self.browser.find_element(By.NAME, "price")
        price_field.send_keys("120")

        description_field = self.browser.find_element(By.NAME, "description")
        description_field.send_keys("Apartamento moderno y bien ubicado.")

        buttons = self.browser.find_elements(By.CSS_SELECTOR, "button[type='submit']")
        for button in buttons:
            if button.text.strip() == "Guardar Apartamento":
                button.click()
                break

        self.assertIn("/add_apartment/", self.browser.current_url)





    def test_createApartment_EmptyForm(self):
        self.browser.get(self.live_server_url)

       
        user_icon = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
        )
        user_icon.click()

        login_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Iniciar sesión"))
        )
        login_button.click()

        email_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_field.send_keys("owner1@example.com")

        password_field = self.browser.find_element(By.NAME, "password")
        password_field.send_keys("owner1_password")

        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
        submit_button.click()

        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        
       
        add_apartment_button = WebDriverWait(self.browser, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.add-property-btn[href='/add_apartment/']"))
        )
        add_apartment_button.click()

        
        self.assertIn("Añadir apartamento", self.browser.page_source)

        buttons = self.browser.find_elements(By.CSS_SELECTOR, "button[type='submit']")
        for button in buttons:
            if button.text.strip() == "Guardar Apartamento":
                button.click()
                break 

        self.assertIn("/add_apartment/", self.browser.current_url)

        
    def test_editApartment(self):
        self.browser.get(self.live_server_url)
        user_icon = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
        )
        user_icon.click()

        login_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Iniciar sesión"))
        )
        login_button.click()

        email_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_field.send_keys("owner1@example.com")

        password_field = self.browser.find_element(By.NAME, "password")
        password_field.send_keys("owner1_password")

        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
        submit_button.click()

        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )


        edit_apartment_button = WebDriverWait(self.browser, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn[href='/edit_apartment/1/']"))
        )
        edit_apartment_button.click()


        self.assertIn("Editar apartamento", self.browser.page_source)


        address_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "address"))
        )
        address_field.clear()
        address_field.send_keys("456 Updated Street")

        guests_field = self.browser.find_element(By.NAME, "guest_count")
        guests_field.clear()
        guests_field.send_keys("6")

        price_field = self.browser.find_element(By.NAME, "price")
        price_field.clear()
        price_field.send_keys("150.00")

        description_field = self.browser.find_element(By.NAME, "description")
        description_field.clear()
        description_field.send_keys("Apartamento actualizado con mejores características.")

        photo_upload = self.browser.find_element(By.NAME, "photos")

        photo_path = os.path.abspath("media/apartments/test/001city_apartment.jpeg")
        photo_upload.send_keys(photo_path)

        buttons = self.browser.find_elements(By.CSS_SELECTOR, "button[type='submit']")
        for button in buttons:
            if button.text.strip() == "Guardar Cambios":
                button.click()
                break
        self.assertIn("/owner_menu/", self.browser.current_url)
        self.assertIn("456 Updated Street", self.browser.page_source)
        self.assertIn("150,00 €", self.browser.page_source)
        self.assertIn("6 huéspedes", self.browser.page_source)

    def test_deleteApartment(self):
        self.browser.get(self.live_server_url)
        user_icon = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fas.fa-user"))
        )
        user_icon.click()

        login_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Iniciar sesión"))
        )
        login_button.click()

        email_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_field.send_keys("owner1@example.com")

        password_field = self.browser.find_element(By.NAME, "password")
        password_field.send_keys("owner1_password")

        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
        submit_button.click()

        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

        delete_account_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-danger[type='submit']"))
        )
        delete_account_button.click()

       
        alert = WebDriverWait(self.browser, 10).until(EC.alert_is_present())
        alert.accept()  

        
        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        self.assertIn("/owner_menu/", self.browser.current_url)
    


