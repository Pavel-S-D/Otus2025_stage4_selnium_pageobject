from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, browser, url, timeout=5):
        self.browser = browser
        self.url = url
        self.timeout = timeout
        self.wait = WebDriverWait(browser, timeout)

    def open(self):
        self.browser.get(self.url)
        return self

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_clickable(self, locator):
        """НОВЫЙ: поиск кликабельного элемента"""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        element = self.find_clickable(locator)  # Используем новый метод
        self.browser.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()
        return self

    def type(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)
        return self

    def is_visible(self, locator, timeout=None):
        """НОВЫЙ: проверка видимости с таймаутом"""
        try:
            wait = WebDriverWait(self.browser, timeout or self.timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False