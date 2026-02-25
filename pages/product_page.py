from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):
    ADD_TO_CART = (By.ID, "button-cart")
    PRICE = (By.CSS_SELECTOR, ".price-new")

    def add_to_cart(self):
        self.click(self.ADD_TO_CART)

    def price_visible(self):
        return self.find(self.PRICE).is_displayed()