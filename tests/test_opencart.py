import time
from selenium.webdriver.common.by import By
from pages.main_page import MainPage
from pages.product_page import ProductPage
from pages.admin_login_page import AdminLoginPage


def test_load_main_page(browser, base_url):
    """ТЕСТ 1: Загрузка главной страницы"""
    browser.get(base_url)
    assert "Your Store" in browser.title


def test_main_page_elements(browser, base_url):
    """ТЕСТ 2: Элементы главной страницы"""
    page = MainPage(browser, base_url).open()
    assert page.logo_visible()
    assert page.search_visible()


def test_catalog_page(browser, base_url):
    """ТЕСТ 3: Страница каталога"""
    browser.get(f"{base_url}/en-gb/catalog/tablet")
    assert "Tablet" in browser.page_source


def test_product_page(browser, base_url):
    """ТЕСТ 4: Страница товара"""
    page = ProductPage(browser, f"{base_url}/en-gb/product/iphone").open()
    assert page.price_visible()
    page.add_to_cart()


def test_login_page(browser, base_url):
    """ТЕСТ 5: Страница входа"""
    browser.get(f"{base_url}/en-gb?route=account/login")
    assert "Returning Customer" in browser.page_source


def test_register_page(browser, base_url):
    """ТЕСТ 6: Страница регистрации"""
    browser.get(f"{base_url}/en-gb?route=account/register")
    assert "Register Account" in browser.page_source


def test_register_new_user(browser, base_url):
    """ТЕСТ 7: Регистрация нового пользователя"""
    browser.get(f"{base_url}/en-gb?route=account/register")
    time.sleep(2)  # Ждем загрузку страницы

    email = f"user_{int(time.time())}@test.com"

    # Заполняем форму
    browser.find_element(By.ID, "input-firstname").send_keys("Test")
    browser.find_element(By.ID, "input-lastname").send_keys("User")
    browser.find_element(By.ID, "input-email").send_keys(email)
    browser.find_element(By.ID, "input-password").send_keys("123456")

    # Скроллим до чекбокса и кликаем
    agree = browser.find_element(By.NAME, "agree")
    browser.execute_script("arguments[0].scrollIntoView(true);", agree)
    time.sleep(1)
    agree.click()

    # Скроллим до кнопки и кликаем
    submit = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    browser.execute_script("arguments[0].scrollIntoView(true);", submit)
    time.sleep(1)
    submit.click()

    time.sleep(3)  # Ждем загрузку страницы успеха
    assert "Your Account Has Been Created!" in browser.page_source


def test_add_to_cart(browser, base_url):
    """ТЕСТ 8: Добавление в корзину"""
    # Открываем страницу iPhone
    browser.get(f"{base_url}/en-gb/product/iphone")
    time.sleep(3)

    # Скроллим до кнопки и ждем
    add_btn = browser.find_element(By.ID, "button-cart")
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_btn)
    time.sleep(1)

    # Кликаем через JavaScript
    browser.execute_script("arguments[0].click();", add_btn)
    time.sleep(3)

    # Переходим в корзину
    browser.get(f"{base_url}/en-gb?route=checkout/cart")
    time.sleep(2)

    assert "iPhone" in browser.page_source


def test_currency_switch(browser, base_url):
    """ТЕСТ 9: Переключение валют"""
    browser.get(base_url)
    time.sleep(3)

    # Получаем цену в долларах
    price1 = browser.find_element(By.CSS_SELECTOR, ".price").text
    print(f"\nUSD: {price1}")

    # Переключаем валюту
    browser.find_element(By.CSS_SELECTOR, "#form-currency .dropdown-toggle").click()
    time.sleep(1)
    browser.find_element(By.CSS_SELECTOR, "a[href*='EUR']").click()
    time.sleep(3)

    # Получаем цену в евро
    price2 = browser.find_element(By.CSS_SELECTOR, ".price").text
    print(f"EUR: {price2}")

    assert price1 != price2


def test_admin_login(browser, base_url, admin_creds):
    """ТЕСТ 10: Вход в админку"""
    login_page = AdminLoginPage(browser, f"{base_url}/administration").open()
    admin_page = login_page.login(admin_creds["login"], admin_creds["password"])
    assert admin_page.is_dashboard()


def test_admin_add_product(browser, base_url, admin_creds, test_product):
    """ТЕСТ 11: Добавление нового товара"""
    # Логин
    browser.get(f"{base_url}/administration")
    time.sleep(2)
    browser.find_element(By.ID, "input-username").send_keys(admin_creds["login"])
    browser.find_element(By.ID, "input-password").send_keys(admin_creds["password"])
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)

    # Переход к товарам
    browser.find_element(By.ID, "menu-catalog").click()
    time.sleep(1)
    browser.find_element(By.LINK_TEXT, "Products").click()
    time.sleep(2)

    # Добавление товара
    browser.find_element(By.CSS_SELECTOR, "a[title='Add New']").click()
    time.sleep(2)

    # General
    browser.find_element(By.ID, "input-name-1").send_keys(test_product["name"])
    browser.find_element(By.ID, "input-meta-title-1").send_keys(test_product["meta_title"])

    # Data
    browser.find_element(By.LINK_TEXT, "Data").click()
    time.sleep(1)
    browser.find_element(By.ID, "input-model").send_keys(test_product["model"])

    # SEO
    browser.find_element(By.LINK_TEXT, "SEO").click()
    time.sleep(1)
    browser.find_element(By.ID, "input-keyword-0-1").send_keys(test_product["seo_keyword"])

    # Save
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)

    # Проверка
    assert "Success" in browser.page_source


def test_admin_delete_product(browser, base_url, admin_creds, test_product):
    """ТЕСТ 12: Удаление товара"""
    # Логин
    browser.get(f"{base_url}/administration")
    time.sleep(2)
    browser.find_element(By.ID, "input-username").send_keys(admin_creds["login"])
    browser.find_element(By.ID, "input-password").send_keys(admin_creds["password"])
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)

    # Переход к товарам
    browser.find_element(By.ID, "menu-catalog").click()
    time.sleep(1)
    browser.find_element(By.LINK_TEXT, "Products").click()
    time.sleep(2)

    # Ищем по названию из фикстуры
    search_input = browser.find_element(By.ID, "input-name")
    search_input.clear()
    search_input.send_keys(test_product["name"])
    browser.find_element(By.ID, "button-filter").click()
    time.sleep(2)

    # Отмечаем чекбокс
    checkbox = browser.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
    checkbox.click()
    time.sleep(1)

    # Удаляем
    delete_btn = browser.find_element(By.CSS_SELECTOR, "button.btn-danger")
    delete_btn.click()
    time.sleep(1)

    browser.switch_to.alert.accept()
    time.sleep(2)

    # Проверяем
    assert "Success" in browser.page_source