from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time


class MainPage(BasePage):
    LOGO = (By.ID, "logo")
    SEARCH = (By.NAME, "search")
    CURRENCY_BTN = (By.CSS_SELECTOR, "#form-currency .dropdown-toggle")
    EURO = (By.CSS_SELECTOR, "a[href*='EUR']")
    PRICE = (By.CSS_SELECTOR, ".price")

    def logo_visible(self):
        return self.find(self.LOGO).is_displayed()

    def search_visible(self):
        return self.find(self.SEARCH).is_displayed()

    def get_price(self):
        prices = self.browser.find_elements(*self.PRICE)
        return prices[0].text if prices else ""

    def switch_to_euro(self):
        # Кликаем на кнопку валюты
        currency_btn = self.browser.find_element(*self.CURRENCY_BTN)
        currency_btn.click()
        time.sleep(1)

        # Кликаем на Euro
        euro = self.browser.find_element(*self.EURO)
        euro.click()
        time.sleep(2)