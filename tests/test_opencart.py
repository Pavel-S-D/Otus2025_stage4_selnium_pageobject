import time
from selenium.webdriver.common.by import By
from pages.main_page import MainPage
from pages.product_page import ProductPage
from pages.admin_login_page import AdminLoginPage
from pages.register_page import RegisterPage


def test_load_main_page(browser, base_url):
    """ТЕСТ 1: Загрузка главной страницы"""
    page = MainPage(browser, base_url).open()
    assert "Your Store" in browser.title
    assert page.cart_visible()
    assert page.menu_visible()


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


def test_register_new_user(browser, base_url, test_user):
    """ТЕСТ 7: Регистрация нового пользователя"""
    register_page = RegisterPage(browser, base_url)
    register_page.open()
    register_page.register(
        first_name=test_user["first_name"],
        last_name=test_user["last_name"],
        email=test_user["email"],
        password=test_user["password"]
    )
    assert register_page.is_registration_successful(), \
        "Сообщение об успешной регистрации не найдено"


def test_add_to_cart(browser, base_url):
    """ТЕСТ 8: Добавление в корзину"""
    product_page = ProductPage(browser, f"{base_url}/en-gb/product/iphone").open()
    product_page.add_to_cart()

    browser.get(f"{base_url}/en-gb?route=checkout/cart")
    assert "iPhone" in browser.page_source


def test_currency_switch(browser, base_url):
    """ТЕСТ 9: Переключение валют"""
    main_page = MainPage(browser, base_url).open()

    price_usd = main_page.get_price()
    print(f"\nUSD: {price_usd}")

    main_page.switch_to_euro()

    price_eur = main_page.get_price()
    print(f"EUR: {price_eur}")

    assert price_usd != price_eur


def test_admin_login(browser, base_url, admin_creds):
    """ТЕСТ 10: Вход в админку"""
    login_page = AdminLoginPage(browser, f"{base_url}/administration").open()
    admin_page = login_page.login(admin_creds["login"], admin_creds["password"])
    assert admin_page.is_dashboard_displayed()


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