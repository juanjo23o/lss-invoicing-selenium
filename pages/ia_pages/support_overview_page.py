from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage


class SupportOverviewPage(BasePage):

    # Selectors
    _BILLING_CYCLE = (By.CSS_SELECTOR, "lssai-select[placeholder='Select Billing Cycle Type']")
    _FIRST_BILLING_CYCLE = (By.XPATH, "//li[text()= 'First - 1 to 30']")
    _SECOND_BILLING_CYCLE = (By.XPATH, "//li[text()= 'Second - 15 to 14']")

    _BILLING_DATE = (By.CSS_SELECTOR, "lssai-select[placeholder='Select Billing Date']")

    _ACCOUNT_NAME = (By.CSS_SELECTOR, "input[placeholder='Select Account']")
    _SUBACCOUNT = (By.CSS_SELECTOR, "input[placeholder='Select Sub Account']")

    _EXPORT_EXCEL = (By.XPATH, "//*[contains(text(), 'Export Excel')]")

    _ASSIGNMENT_LOGO = (By.XPATH, "//span[text()= ' assignment ']")
    _OVERVIEW_SECTION = (By.XPATH, "//span[text()= 'Support Overview']")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def isAtOverviewPage(self):
        super().isAt(self._EXPORT_EXCEL)
        return self

    def navigate_to_overview_page(self):
        super().wait_for_element_visibility(self._ASSIGNMENT_LOGO)
        super().do_click(self._ASSIGNMENT_LOGO)
        super().do_click(self._ASSIGNMENT_LOGO)
        super().do_click(self._OVERVIEW_SECTION)
        return self

    def select_billing_cycle(self, billing_cycle: int):
        super().do_click(self._BILLING_CYCLE)
        if billing_cycle == 1:
            super().do_click(self._FIRST_BILLING_CYCLE)
        elif billing_cycle == 2:
            super().do_click(self._SECOND_BILLING_CYCLE)
        return self

    def select_billing_date(self, billing_date: str):
        super().do_click(self._BILLING_DATE)
        super().do_click((By.XPATH, f"//li[text()= '{billing_date}']"))
        return self

    def select_account(self, account: str, index: str):
        super().send_keys(self._ACCOUNT_NAME, account)
        if index and isinstance(index, int):
            super().do_click((By.XPATH, f"(//mat-option[@role='option'])[{index}]"))
        else:
            super().do_click((By.XPATH, "//mat-option[@role='option']"))
        sleep(0.5)
        return self

    def select_subaccount(self, subaccount: str, index: str):
        super().send_keys(self._SUBACCOUNT, subaccount)
        if index and isinstance(index, int):
            super().do_click((By.XPATH, f"(//mat-option[@role='option'])[{index}]"))
        else:
            super().do_click((By.XPATH, "//mat-option[@role='option']"))
        return self

    def click_export_excel(self):
        super().do_click(self._EXPORT_EXCEL)
        return self
