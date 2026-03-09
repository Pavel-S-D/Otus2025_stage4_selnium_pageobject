from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC


class MainPage(BasePage):
    LOGO = (By.ID, "logo")
    SEARCH = (By.NAME, "search")
    CURRENCY_BTN = (By.CSS_SELECTOR, "#form-currency .dropdown-toggle")
    EURO = (By.CSS_SELECTOR, "a[href*='EUR']")
    PRICE = (By.CSS_SELECTOR, ".price")
    CART = (By.ID, "header-cart")
    MENU = (By.CSS_SELECTOR, ".navbar")

    def logo_visible(self):
        return self.find(self.LOGO).is_displayed()

    def search_visible(self):
        return self.find(self.SEARCH).is_displayed()

    def cart_visible(self):
        try:
            return self.find(self.CART).is_displayed()
        except:
            return False

    def menu_visible(self):
        try:
            return self.find(self.MENU).is_displayed()
        except:
            return False

    def get_price(self):
        prices = self.browser.find_elements(*self.PRICE)
        return prices[0].text if prices else ""

    def switch_to_euro(self):
        """Переключение на евро с ожиданиями вместо sleep"""
        currency_btn = self.wait.until(EC.element_to_be_clickable(self.CURRENCY_BTN))
        currency_btn.click()

        euro = self.wait.until(EC.element_to_be_clickable(self.EURO))
        euro.click()

        try:
            self.wait.until(EC.staleness_of(self.find(self.PRICE)))
        except:
            pass

        return self