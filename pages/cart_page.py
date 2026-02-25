from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    PRODUCT = (By.LINK_TEXT, "iPhone")

    def has_product(self):
        return self.find(self.PRODUCT).is_displayed()