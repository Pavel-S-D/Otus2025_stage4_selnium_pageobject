from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class AdminPage(BasePage):
    # Локаторы
    DASHBOARD = (By.XPATH, "//h1[contains(text(),'Dashboard')]")
    CATALOG = (By.ID, "menu-catalog")
    PRODUCTS = (By.LINK_TEXT, "Products")
    ADD_NEW = (By.CSS_SELECTOR, "[data-original-title='Add New']")
    PROD_NAME = (By.ID, "input-name-1")
    META_TITLE = (By.ID, "input-meta-title-1")
    DATA_TAB = (By.LINK_TEXT, "Data")
    MODEL = (By.ID, "input-model")
    SAVE = (By.CSS_SELECTOR, "button[type='submit']")
    SUCCESS = (By.CSS_SELECTOR, ".alert-success")
    FILTER_NAME = (By.ID, "input-name")
    FILTER_BTN = (By.ID, "button-filter")
    DELETE = (By.CSS_SELECTOR, "[data-original-title='Delete']")

    def wait_click(self, locator, timeout=10):
        """Ожидание кликабельного элемента"""
        return WebDriverWait(self.browser, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_visible(self, locator, timeout=10):
        """Ожидание видимого элемента"""
        return WebDriverWait(self.browser, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def is_dashboard_displayed(self):
        """Проверка наличия дашборда"""
        try:
            return self.wait_visible(self.DASHBOARD, 5).is_displayed()
        except:
            return False

    def go_to_products(self):
        """Переход в раздел Products"""
        self.wait_click(self.CATALOG).click()
        self.wait_visible(self.PRODUCTS)
        self.wait_click(self.PRODUCTS).click()

    def add_product(self, name, model):
        """Добавление продукта"""
        self.wait_click(self.ADD_NEW).click()

        self.wait_visible(self.PROD_NAME).send_keys(name)
        self.find(self.META_TITLE).send_keys(name)

        self.wait_click(self.DATA_TAB).click()
        self.wait_visible(self.MODEL).send_keys(model)
        self.wait_click(self.SAVE).click()

    def find_product(self, name):
        """Поиск продукта по имени"""
        self.wait_visible(self.FILTER_NAME).clear()
        self.find(self.FILTER_NAME).send_keys(name)
        self.wait_click(self.FILTER_BTN).click()

    def delete_product(self, name):
        """Удаление продукта"""
        self.find_product(name)

        self.wait_click((By.CSS_SELECTOR, "input[type='checkbox']")).click()
        self.wait_click(self.DELETE).click()

        WebDriverWait(self.browser, 5).until(EC.alert_is_present())
        self.browser.switch_to.alert.accept()

        # Ждем исчезновения чекбокса
        WebDriverWait(self.browser, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "input[type='checkbox']"))
        )

    def success_message(self):
        """Проверка сообщения об успехе"""
        try:
            return self.wait_visible(self.SUCCESS, 5).is_displayed()
        except:
            return False