from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from helpers.read_document import SdHandler
from pages.base_page import BasePage
from helpers.text_formatter import TextFormatter
import json
import os
from fuzzywuzzy import fuzz


class RatesPage(BasePage):
    _SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Search']")
    _EMPLOYEE_NAME = (By.CSS_SELECTOR, "div[class='mat-tooltip-trigger rate-data__name']")
    _EMPLOYEE_STATUS = (By.CSS_SELECTOR, "span[class='rate-data__status']")
    _EMPLOYEE_STATUS_DATE = (By.CSS_SELECTOR, "span[class='rate-data__status-date']")
    _EMPLOYEE_POSITION = (By.CSS_SELECTOR, "span[class='mat-tooltip-trigger rate-data__position']")
    _EMPLOYEE_ACCOUNT = (By.CSS_SELECTOR, "span[class='mat-tooltip-trigger rate-data__account']")
    _EMPLOYEE_RATE = (By.CSS_SELECTOR, "div[class='monthly-rate__container'] > input")
    _EMPLOYEE_RATE_ADJ_DATE = (By.CSS_SELECTOR, "div[class='calendar__container'] > input")
    _CROSS_BUTTON = (By.XPATH, "(//button[@aria-label='Clear'])[2]")


    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def isAtRatesSection(self):
        super().isAt(self._EMPLOYEE_NAME)
        super().wait_for_element_visibility(self._EMPLOYEE_NAME)
        return self

    def navigate_to_rates_section(self, url: str):
        self.driver.get(url)
        return self

    def look_up_employee(self, employee: str):
        super().do_click(self._SEARCH_INPUT)
        super().send_keys(self._SEARCH_INPUT, employee)
        super().press_enter(self._SEARCH_INPUT)

    def get_and_assert_name(self, name: str):
        portal_name = super().get_text(self._EMPLOYEE_NAME)
        ratio = fuzz.ratio(portal_name, name)
        if portal_name == name:
            return ''
        elif ratio > 80:
            return ''
        else:
            return f"Please check out the following difference, Portal: {portal_name} + IA: {name}"

    def get_and_assert_status(self, status: str):
        portal_status = super().get_text(self._EMPLOYEE_STATUS)
        ratio = fuzz.ratio(portal_status.lower(), status)
        if ratio > 90:
            return ''
        else:
            return f"Please check out the following difference, Portal: {portal_status} + IA: {status}"

    def get_and_assert_status_date(self, status_date: str):
        portal_status_date = super().get_text(self._EMPLOYEE_STATUS_DATE)
        portal_status_date_formatted = TextFormatter.format_rate(portal_status_date)
        if portal_status_date_formatted == status_date:
            return ''
        else:
            return f"Please check out the following difference, Portal: {portal_status_date} + IA: {status_date}"

    def get_and_assert_position(self, position: str):
        portal_position = super().get_text(self._EMPLOYEE_POSITION)
        ratio = fuzz.ratio(portal_position, position)
        if portal_position.lower() == position.lower():
            return ''
        elif ratio > 80:
            return ''
        else:
            return f"Please check out the following difference, Portal: {portal_position.lower()} + IA: {position.lower()}"

    def get_and_assert_account(self, account: str):
        portal_account = super().get_text(self._EMPLOYEE_ACCOUNT)
        ratio = fuzz.ratio(portal_account, account)
        if account in portal_account:
            return ''
        elif ratio > 70:
            return ''
        else:
            return f"Please check out the following difference, Portal: {portal_account} -- IA: {account}"

    def get_and_assert_rate(self, rate: str):
        portal_rate = super().get_value(self._EMPLOYEE_RATE)
        portal_rate_formatted = TextFormatter.format_rate(portal_rate)
        if portal_rate_formatted == rate:
            return ''
        else:
            return f"Please check out the following difference, Portal: {portal_rate_formatted} + IA: {rate}"

    def get_and_assert_rate_adj_date(self, rate_adj_date: str):
        portal_rate_adj_date = super().get_value(self._EMPLOYEE_RATE_ADJ_DATE)
        if portal_rate_adj_date == '':
            portal_rate_adj_date_formatted = 'empty'
        else:
            portal_rate_adj_date_formatted = TextFormatter.format_rate_adj_date(portal_rate_adj_date)
        if portal_rate_adj_date_formatted == rate_adj_date:
            return ''
        else:
            return f"Please check out the following difference, Portal: {portal_rate_adj_date_formatted} + IA: {rate_adj_date}"

    def look_up_employee_and_assert(self, employee_list, employee_ids_list, account_name, sub_account):
        employee_results = {}
        name = ''
        account = ''
        status = ''
        status_date = ''
        position = ''
        rate = ''
        rate_adj_date = ''
        counter: int = 0
        employee_results[sub_account] = {}
        for employee_id in employee_ids_list:
            employee_data = SdHandler.get_employee_data_by_id(employee_list, employee_id)
            try:
                self.look_up_employee(employee_id)
                sleep(1)
                super().wait_for_element_visibility((By.XPATH, f"//*[text()='{employee_id}']"))
                name = self.get_and_assert_name(employee_data['name'])
                status = self.get_and_assert_status(employee_data['status'])
                status_date = self.get_and_assert_status_date(employee_data['active_date'])
                position = self.get_and_assert_position(employee_data['title'])
                account = self.get_and_assert_account(account_name)
                rate = self.get_and_assert_rate(employee_data['rate'])
                rate_adj_date = self.get_and_assert_rate_adj_date(employee_data['rate_adj_date'])
            except:
                if employee_data['status'] == "Removed":
                    name = ''
                    account = ''
                    status = employee_data['status']
                    status_date = ''
                    position = ''
                    rate = ''
                    rate_adj_date = ''
                    pass
                    # super().do_click(self._CROSS_BUTTON)
                    # super().wait_for_element_visibility(self._EMPLOYEE_NAME)
                    # sleep(2.5)
                    # continue
                else:pass
            if name == '' and account == '' and status == '' and position == '' and rate == '' and rate_adj_date == '' and status_date == '':
                super().do_click(self._CROSS_BUTTON)
                super().wait_for_element_visibility(self._EMPLOYEE_NAME)
                sleep(2.5)
                continue
            else:
                employee_results[sub_account][counter] = {
                    "employee_id": employee_id,
                    "name": name,
                    "account": account,
                    "status": status,
                    "status_date": status_date,
                    "position": position,
                    "rate": rate,
                    "rate_adj_date": rate_adj_date}
                if status == 'Removed':
                    pass
                else:
                    counter += 1
                try:
                    with open(os.getenv('PATH_RESULTS'), 'r') as f:
                        data = json.load(f)
                except:
                    data = {}

                data.update(employee_results)

                with open(os.getenv('PATH_RESULTS'), 'w') as f:
                    json.dump(data, f)
            super().do_click(self._CROSS_BUTTON)
            super().wait_for_element_visibility(self._EMPLOYEE_NAME)
            sleep(2.5)
        return counter
