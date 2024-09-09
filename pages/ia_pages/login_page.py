from pages.ia_pages.support_overview_page import SupportOverviewPage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage


class LoginPage(BasePage):
    _EMAIL_INPUT = (By.CSS_SELECTOR, "input[placeholder='Email address']")
    _PASSWORD_INPUT = (By.CSS_SELECTOR, "input[placeholder='Password']")

    _LOGIN_CLICK = (By.XPATH, "//*[contains(text(), ' Log in ')]")
    _CONTINUE_BUTTON = (By.XPATH, "//*[contains(text(), ' Continue ')]")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def isAtLoginPage(self):
        super().isAt(self._LOGIN_CLICK)
        return self

    def navigate_to(self, url: str):
        self.driver.get(url)
        return self

    def login(self):
        super().do_click(self._LOGIN_CLICK)
        super().send_keys(self._EMAIL_INPUT, "jospinad+1@lean-tech.io")
        super().send_keys(self._PASSWORD_INPUT, "Juanjose1,.-")
        super().do_click(self._LOGIN_CLICK)
        try:
            super().wait_for_element_visibility(self._CONTINUE_BUTTON)
            super().do_click(self._CONTINUE_BUTTON)
        except:
            pass
        return SupportOverviewPage(self.driver)
