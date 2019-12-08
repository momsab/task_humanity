from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class LoginPage:

    INPUT_USER = (By.ID, 'email')
    INPUT_PASSWORD = (By.ID, 'password')
    DIV_MESSAGE = (By.ID, 'response-message')
    BUTTON_LOGIN = (By.NAME, 'login')

    def __init__(self,
                 browser):
        self.browser = browser

    def load(self,
             url):
        self.browser.get(url)

    def fill_username(self,
                      username):

        WebDriverWait(self.browser, 1).until(ec.visibility_of_element_located(self.INPUT_USER)).send_keys(username)

    def fill_password(self,
                      password):
        WebDriverWait(self.browser, 1).until(ec.visibility_of_element_located(self.INPUT_PASSWORD)).send_keys(password)

    def click_login(self):
        WebDriverWait(self.browser, 1).until(ec.visibility_of_element_located(self.BUTTON_LOGIN)).click()

    def check_login_message(self,
                            text):
        return WebDriverWait(self.browser, 3,
                             poll_frequency=0.5).until(ec.text_to_be_present_in_element(self.DIV_MESSAGE,
                                                                                        text))
