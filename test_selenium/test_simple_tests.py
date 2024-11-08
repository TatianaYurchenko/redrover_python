import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
@pytest.fixture
def chrome_options():
    options = Options()
    options.add_argument('--start-maximized')
    return options

@pytest.fixture
def driver(chrome_options):
    driver = webdriver.Chrome(options=chrome_options)
    return driver

@pytest.fixture
def wait(driver):
    wait = WebDriverWait(driver, timeout=10)
    return wait


def test_one(driver, wait):
    driver.get("http://195.133.27.184/")
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(("xpath", "(//a[@href='/list/'])[2]")))
    assert element.is_displayed()
    element.click()
    assert driver.current_url == "http://195.133.27.184/list/", "Wrong URL"

def test_chek_the_registration_functionality(driver, wait):
    driver.get("https://victoretc.github.io/selenium_waits/")
    title_h1 = driver.find_element("xpath", "//h1")
    assert title_h1.text == "Практика с ожиданиями в Selenium"
    btn_start_testing = wait.until(EC.element_to_be_clickable(("xpath", "//button[@id='startTest']")))
    btn_start_testing.click()
    input_login = driver.find_element("xpath", "//input[@id='login']")
    input_login.clear()
    input_login.send_keys("login")
    input_password = driver.find_element("xpath", "//input[@id='password']")
    input_password.clear()
    input_password.send_keys("password")
    driver.find_element("xpath", "//input[@id='agree']").click()
    driver.find_element("xpath", "//button[@id='register']").click()
    spinner = wait.until(EC.visibility_of_element_located(("xpath", "//div[@id='loader']")))
    assert spinner.is_displayed()
    success_message = wait.until(EC.visibility_of_element_located(("xpath", "//p[@id='successMessage']")))
    assert success_message.text == 'Вы успешно зарегистрированы!'





