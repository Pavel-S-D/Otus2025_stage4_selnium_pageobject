from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time


class AdminPage(BasePage):
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

    def is_dashboard(self):
        return self.find(self.DASHBOARD).is_displayed()

    def go_to_products(self):
        self.click(self.CATALOG)
        time.sleep(1)
        self.click(self.PRODUCTS)
        time.sleep(2)

    def add_product(self, name, model):
        self.click(self.ADD_NEW)
        time.sleep(2)

        self.type(self.PROD_NAME, name)
        self.type(self.META_TITLE, name)

        self.click(self.DATA_TAB)
        time.sleep(1)

        self.type(self.MODEL, model)

        self.click(self.SAVE)
        time.sleep(2)

    def find_product(self, name):
        self.type(self.FILTER_NAME, name)
        self.click(self.FILTER_BTN)
        time.sleep(2)

    def delete_product(self, name):
        self.find_product(name)

        checkbox = self.browser.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
        checkbox.click()
        time.sleep(1)

        self.click(self.DELETE)
        time.sleep(1)

        alert = self.browser.switch_to.alert
        alert.accept()
        time.sleep(2)

    def success_message(self):
        try:
            return self.find(self.SUCCESS).is_displayed()
        except Exception:
            return False