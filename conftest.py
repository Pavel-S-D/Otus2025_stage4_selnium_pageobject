import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait


def pytest_addoption(parser):
    parser.addoption("--url", default="192.168.63.184:8084", help="OpenCart URL")


@pytest.fixture
def browser():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def base_url(request):
    url = request.config.getoption("--url")
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return url


@pytest.fixture
def wait(browser):
    return WebDriverWait(browser, 5)


@pytest.fixture
def admin_creds():
    return {"login": "user", "password": "bitnami"}

@pytest.fixture
def test_product():
    return {
        "name": "Test_product",
        "model": "Test_model",
        "meta_title": "Meta Test_product",
        "seo_keyword": "test-product"
    }

@pytest.fixture
def test_user():
    return {
        "first_name": "Test",
        "last_name": "User",
        "email": f"user_{int(time.time())}@test.com",
        "password": "123456"
    }