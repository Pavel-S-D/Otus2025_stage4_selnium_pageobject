from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    NEW_CUSTOMER_HEADER = (By.XPATH, "//h2[contains(text(),'New Customer')]")
    FORM_LABELS = (By.CSS_SELECTOR, "label.col-form-label")

    def new_customer_header_is_displayed(self):
        return self.find(self.NEW_CUSTOMER_HEADER).is_displayed()

    def form_labels_are_displayed(self):
        return self.find(self.FORM_LABELS).is_displayed()