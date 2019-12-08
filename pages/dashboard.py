from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DashboardPage:

    LINK_STAFF = (By.ID, 'sn_staff')
    TITLE_PART = 'Dashboard'

    def __init__(self,
                 browser):
        self.browser = browser

    def check_title(self):
        return WebDriverWait(self.browser, 20,
                             poll_frequency=1).until(EC.title_contains(self.TITLE_PART))

    def click_staff(self):
        WebDriverWait(self.browser, 20,
                      poll_frequency=1).until(EC.visibility_of_element_located(self.LINK_STAFF)).click()


