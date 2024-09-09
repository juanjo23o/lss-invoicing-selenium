from time import sleep

from selenium.webdriver import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def isAt(self, locator: tuple):
        wait = WebDriverWait(self.driver, 15)
        assert wait.until(EC.visibility_of_element_located(locator)).is_displayed().__eq__(True)

    def send_keys(self, locator: tuple, string: str):
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.visibility_of_element_located(locator)).send_keys(string)

    def do_click(self, locator: tuple):
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.visibility_of_element_located(locator)).click()

    def get_text(self, locator: tuple) -> str:
        wait = WebDriverWait(self.driver, 15)
        return wait.until(EC.visibility_of_element_located(locator)).text

    def get_value(self, locator: tuple) -> str:
        wait = WebDriverWait(self.driver, 15)
        return wait.until(EC.visibility_of_element_located(locator)).get_attribute('value')

    def wait_for_element_visibility(self, locator: tuple):
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.visibility_of_element_located(locator))

    def press_enter(self, locator: tuple):
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.visibility_of_element_located(locator)).send_keys(Keys.ENTER)

