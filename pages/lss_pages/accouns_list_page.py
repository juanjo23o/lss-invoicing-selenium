from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage


class AccountListPage(BasePage):
    _SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Search']")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def navigate_to_account_section(self, url: str):
        self.driver.get(url)
        return self

    def isAtAccountSection(self):
        super().isAt(self._SEARCH_INPUT)
        return self

    def return_total_employees(self, index) -> dict:
        if index and isinstance(index, int):
            return {
                'total':super().get_text(
                (By.XPATH, f"(//tr[@class='ng-star-inserted']//td[4]//div[@class='employee-counter']/span)[{index}]")),
                'Active':super().get_text(
                (By.XPATH, f"(//tr[@class='ng-star-inserted']//td[4]//div[@class='employee-counter'])[{index}]/div/div[1]")),
                'Assigned':super().get_text(
                (By.XPATH, f"(//tr[@class='ng-star-inserted']//td[4]//div[@class='employee-counter'])[{index}]/div/div[2]")),
                'Active Floater':super().get_text(
                (By.XPATH, f"(//tr[@class='ng-star-inserted']//td[4]//div[@class='employee-counter'])[{index}]/div/div[3]")),
                'Free Floater':super().get_text(
                (By.XPATH, f"(//tr[@class='ng-star-inserted']//td[4]//div[@class='employee-counter'])[{index}]/div/div[4]"))
            }
        else:
            return {
                'total':super().get_text((By.CSS_SELECTOR,
                                     "tr[class='ng-star-inserted'] > td:nth-child(4) > div [class='employee-counter'] > span")),
                'Active':super().get_text((By.CSS_SELECTOR,
                                     "tr[class='ng-star-inserted'] > td:nth-child(4) > div [class='employee-counter'] > div > div:nth-child(1)")),
                'Assigned':super().get_text((By.CSS_SELECTOR,
                                     "tr[class='ng-star-inserted'] > td:nth-child(4) > div [class='employee-counter'] > div > div:nth-child(2)")),
                'Active Floater':super().get_text((By.CSS_SELECTOR,
                                     "tr[class='ng-star-inserted'] > td:nth-child(4) > div [class='employee-counter'] > div > div:nth-child(3)")),
                'Free Floater':super().get_text((By.CSS_SELECTOR,
                                     "tr[class='ng-star-inserted'] > td:nth-child(4) > div [class='employee-counter'] > div > div:nth-child(4)"))
            }

    def wait_for_render(self):
        super().wait_for_element_visibility((By.CSS_SELECTOR, "tbody[class='p-element p-datatable-tbody']"))
        return self

    def look_up_account(self, account: str):
        super().do_click(self._SEARCH_INPUT)
        super().send_keys(self._SEARCH_INPUT, account)
        super().press_enter(self._SEARCH_INPUT)
        return self
