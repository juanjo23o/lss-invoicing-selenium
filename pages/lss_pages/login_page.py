from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
from pages.lss_pages.accouns_list_page import AccountListPage


class LoginLssPage(BasePage):

    _EMPLOYEE_BUTTON = (By.ID, "employeeButton")
    _EMAIL_INPUT = (By.ID, "emailField")
    _PASSWORD_INPUT = (By.ID, "passwordField")
    _ARROW_LOGO = (By.ID, "login")
    _LETS_GO_BUTTON = (By.ID, "letsGoButton")
    _BILLING_BUTTON = (By.CSS_SELECTOR, "div[class='app-card ng-star-inserted']:nth-child(2)")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def navigate_to(self, url: str):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(url)
        return self

    def click_on_employee_button(self):
        super().wait_for_element_visibility(self._EMPLOYEE_BUTTON)
        super().do_click(self._EMPLOYEE_BUTTON)
        return self

    def login(self):
        super().do_click(self._EMAIL_INPUT)
        super().send_keys(self._EMAIL_INPUT, "oalvarez@lean-tech.io")
        super().do_click(self._ARROW_LOGO)
        super().wait_for_element_visibility(self._PASSWORD_INPUT)
        super().send_keys(self._PASSWORD_INPUT, "F3l1p301$2025")
        super().do_click(self._LETS_GO_BUTTON)
        try:
            super().wait_for_element_visibility(self._BILLING_BUTTON)
            super().do_click(self._BILLING_BUTTON)
        except:
            pass
        return AccountListPage(self.driver)


