from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class StaffPage:

    BUTTON_ADD_EMPLOYEE = (By.ID, 'act_primary')

    def __init__(self,
                 browser):
        self.browser = browser

    def click_add_employee(self):
        WebDriverWait(self.browser, 20,
                      poll_frequency=1).until(EC.visibility_of_element_located(self.BUTTON_ADD_EMPLOYEE)).click()
