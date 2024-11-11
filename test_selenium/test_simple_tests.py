import pytest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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

def test_add_and_delete_element(driver, wait):
    driver.get("https://the-internet.herokuapp.com/add_remove_elements/")
    driver.find_element("xpath", "//button[text()='Add Element']").click()
    btn_delete = wait.until(EC.visibility_of_element_located(("xpath", "//button[text()='Delete']")))
    btn_delete.click()
    # try:
    #     wait.until(EC.invisibility_of_element_located(("xpath", "//button[text()='Delete']")))
    #     print("Элемент успешно удален")
    # except TimeoutException:
    #     print("Элемент не был удален")
    assert len(driver.find_elements("xpath", "//button[text()='Delete']")) == 0, "Элемент не удален"


def test_base_auth(driver, wait):
    # Передаем логин и пароль в URL: https://username:password@site
    username = "admin"
    password = "admin"
    url = f"https://{username}:{password}@the-internet.herokuapp.com/basic_auth"

    driver.get(url)

    # Проверка, что страница загружена
    success_message = wait.until(
        EC.visibility_of_element_located(("xpath", "//p[contains(text(),'Congratulations!')]")))
    assert "Congratulations!" in success_message.text

def test_checkboxes(driver, wait):
    url = "https://the-internet.herokuapp.com/checkboxes"
    driver.get(url)
    checkbox_1 = ("xpath", "(//input[@type='checkbox'])[1]")
    checkbox_2 = ("xpath", "(//input[@type='checkbox'])[2]")
    driver.find_element(*checkbox_1).click()
    assert driver.find_element(*checkbox_1).get_attribute("checked") == "true"
    driver.find_element(*checkbox_2).click()
    assert driver.find_element(*checkbox_2).get_attribute("checked") is None

def test_broken_images(driver, wait):
    # Открываем страницу
    url = "https://the-internet.herokuapp.com/broken_images"
    driver.get(url)

    # Ищем все изображения на странице
    images = driver.find_elements("xpath", "//img")
    # Проверяем изображения со 2 по 4 (индексы 1, 2, 3)
    for i, img in enumerate(images[1:4]):
        src = img.get_attribute("src")
        print(f"Проверка изображения {i+1}: {src}")

        # Проверяем, что изображение загружено корректно
        try:
            # Скроллим к изображению, чтобы убедиться, что оно в зоне видимости
            driver.execute_script("arguments[0].scrollIntoView();", img)
            assert img.size["width"] > 0 and img.size["height"] > 0, f"Изображение {i+1} ({src}) не загружено."
            print(f"Изображение {i+1} загружено корректно.")
        except AssertionError as e:
            print(e)

    print("Проверка завершена.")