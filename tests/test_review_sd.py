from helpers.read_document import SdHandler
from helpers.help_my_locator import HelpMyLocator
from helpers.utilities import generate_employees_report, generate_accounts_report
from tests.test_data import second_cycle_accounts, first_cycle_accounts
from pages.ia_pages.login_page import LoginPage
from pages.lss_pages.login_page import LoginLssPage
from pages.lss_pages.rates_page import RatesPage
from time import sleep
import pytest
import json
import os

accounts_list = [(k, v["legal_name"], v["account_name"], v["sub_account"]) for k, v in
                 first_cycle_accounts.accounts.items()]


class TestReviewMainFlow:
    @pytest.mark.parametrize("account_id, legal_name, account_name, sub_account", accounts_list)
    def test_go_to(self, set_up, account_id, legal_name, account_name, sub_account):
        account_index = HelpMyLocator.identify_index(account_name)
        sub_account_index = HelpMyLocator.identify_index(sub_account)
        legal_account_index = HelpMyLocator.identify_index(legal_name)
        account_name = account_name.split("-")[0]
        sub_account = sub_account.split("-")[0]
        legal_name = legal_name.split("-")[0]
        account_result = {}
        login_page = LoginPage(set_up)
        lss_page = LoginLssPage(set_up)
        lss_rates_page = RatesPage(set_up)
        (login_page
         .navigate_to(os.getenv('IA_URL'))
         .isAtLoginPage()
         .login()
         .navigate_to_overview_page()
         .isAtOverviewPage()
         .select_billing_cycle(int(os.getenv('BILLING_CYCLE')))
         .select_billing_date(os.getenv('BILLING_DATE'))
         .select_account(account_name, account_index)
         .select_subaccount(sub_account, sub_account_index)
         .click_export_excel())
        sleep(2)
        employees = SdHandler.extract_sdm_information(sub_account)
        print(employees)
        employee_ids = SdHandler.get_all_employee_ids(employees)
        total_employees = (lss_page
                           .navigate_to('https://portal.leangroup.com/portal')
                           .click_on_employee_button()
                           .login()
                           .navigate_to_account_section('https://billing.leangroup.com/accounts')
                           .isAtAccountSection()
                           .wait_for_render()
                           .look_up_account(legal_name)
                           .wait_for_render()
                           .return_total_employees(legal_account_index))
        status_employee_counter = SdHandler.get_employees_by_status(employees)
        employee_with_issues = (lss_rates_page
                                .navigate_to_rates_section('https://billing.leangroup.com/rates')
                                .isAtRatesSection()
                                .look_up_employee_and_assert(employees, employee_ids, account_name, sub_account))
        account_result[sub_account] = {
            "Employees with Issues": employee_with_issues,
            "Total Employees": f"Portal total employees {total_employees['total']}, IA total employees {SdHandler.get_total_employees(employees)}",
            "Active Employees": f"Portal active employees {total_employees['Active']}, IA total employees {status_employee_counter['Active']}"
        }
        try:
            with open(os.getenv('PATH_ACCOUNTS_RESULTS'), 'r') as f:
                data = json.load(f)
        except:
            data = {}

        data.update(account_result)

        with open(os.getenv('PATH_ACCOUNTS_RESULTS'), 'w') as f:
            json.dump(data, f)
        sleep(3)

    def test_generate_reports(self):
        with open(r"C:\Users\Usuario\Desktop\ia-invoicing-selenium\tests\test_results\employees_results.json", 'r') as json_file:
            data = json.load(json_file)
        generate_employees_report(data)
        with open(r"C:\Users\Usuario\Desktop\ia-invoicing-selenium\tests\test_results\accounts_results.json", 'r') as json_file:
            data = json.load(json_file)
        generate_accounts_report(data)
