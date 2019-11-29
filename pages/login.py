import time
from selenium.webdriver.common.by import By


class LoginPage:

    URL = 'https://www.humanity.com/app/'
    INPUT_USER = (By.ID, 'email')
    INPUT_PASSWORD = (By.ID, 'password')
    DIV_MESSAGE = (By.ID, 'response-message')
    BUTTON_LOGIN = (By.NAME, 'login')

    def __init__(self,
                 browser):
        self.browser = browser

    def load(self):
        self.browser.get(self.URL)

    def signin(self,
               username,
               password):

        username_input = self.browser.find_element(*self.INPUT_USER)
        username_input.send_keys(username)
        password_input = self.browser.find_element(*self.INPUT_PASSWORD)
        password_input.send_keys(password)
        login_button = self.browser.find_element(*self.BUTTON_LOGIN)
        login_button.click()
        message_div = self.browser.find_element(*self.DIV_MESSAGE)

        time.sleep(3)

        return message_div.get_attribute('innerHTML').lower()

