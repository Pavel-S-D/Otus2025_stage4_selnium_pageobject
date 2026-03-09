from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.admin_page import AdminPage


class AdminLoginPage(BasePage):
    USERNAME = (By.ID, "input-username")
    PASSWORD = (By.ID, "input-password")
    LOGIN_BTN = (By.CSS_SELECTOR, "button[type='submit']")

    def login(self, user, pwd):
        self.type(self.USERNAME, user)
        self.type(self.PASSWORD, pwd)
        self.click(self.LOGIN_BTN)
        return AdminPage(self.browser, self.url)