from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):
    ADD_TO_CART = (By.ID, "button-cart")
    PRICE = (By.CSS_SELECTOR, ".price-new")
    CART_SUCCESS = (By.CSS_SELECTOR, ".alert-success")  # Добавили локатор

    def add_to_cart(self):
        """Добавление в корзину с ожиданием"""
        self.click(self.ADD_TO_CART)
        try:
            self.wait.until(EC.visibility_of_element_located(self.CART_SUCCESS))
        except:
            pass
        return self

    def price_visible(self):
        return self.find(self.PRICE).is_displayed()