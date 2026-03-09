from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class RegisterPage(BasePage):
    # Локаторы
    FIRST_NAME = (By.ID, "input-firstname")
    LAST_NAME = (By.ID, "input-lastname")
    EMAIL = (By.ID, "input-email")
    PASSWORD = (By.ID, "input-password")
    AGREE = (By.NAME, "agree")
    SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "#content h1")

    def open(self):
        """Открыть страницу регистрации"""
        self.browser.get(f"{self.url}/en-gb?route=account/register")
        return self

    def register(self, first_name, last_name, email, password):
        """Заполнить форму регистрации и отправить"""
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.EMAIL, email)
        self.type(self.PASSWORD, password)

        agree = self.find(self.AGREE)
        agree.location_once_scrolled_into_view
        agree.click()

        submit = self.find(self.SUBMIT)
        submit.location_once_scrolled_into_view
        submit.click()

        return self

    def wait_for_success_page(self, timeout=5):
        """Ожидание загрузки страницы успеха"""
        self.wait.until(
            EC.url_contains("route=account/success")
        )
        return self

    def is_registration_successful(self, timeout=5):
        """Проверка успешность регистрации с ожиданием"""
        try:
            self.wait.until(
                EC.url_contains("route=account/success")
            )
            message = self.wait.until(
                EC.visibility_of_element_located(self.SUCCESS_MESSAGE)
            )
            return "Your Account Has Been Created!" in message.text
        except:
            return False