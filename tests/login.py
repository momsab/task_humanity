from random import randint
import pytest
from selenium import webdriver
from data.data import Data
from pages.login import LoginPage
from pages.dashboard import DashboardPage
import utilities

data = Data


@pytest.fixture
def browser():

    driver = webdriver.Chrome(data.CHROME_DRIVER_PATH)
    yield driver
    driver.maximize_window()
    driver.quit()


@pytest.mark.parametrize(
    "user_name, pass_word",
    [
        pytest.param(
            data.LOGIN_EMAIL,
            data.LOGIN_PASSWORD,
            id='1_login_with_correct_data'
        ),
        pytest.param(
            data.LOGIN_EMAIL.swapcase(),
            data.LOGIN_PASSWORD,
            id='2_login_with_case_changed_email'
        ),
    ]
)
def testing_with_correct_data(browser,
                              user_name,
                              pass_word):
    login_page = LoginPage(browser)
    login_page.load(url=data.LOGIN_URL)
    login_page.fill_username(user_name)
    login_page.fill_password(pass_word)
    login_page.click_login()

    dashboard_page = DashboardPage(browser)
    title_has_part = dashboard_page.check_title()

    assert title_has_part is True


@pytest.mark.parametrize(
    "user_name, pass_word",
    [
        pytest.param(
            '',
            '',
            id='3_login_with_empty_data'
        ),
        pytest.param(
            '',
            data.LOGIN_PASSWORD,
            id='4_login_with_empty_email'
        ),
        pytest.param(
            data.LOGIN_EMAIL,
            '',
            id='5_login_with_empty_password'
        ),
        pytest.param(
            utilities.generate_random_email(data.LOGIN_EMAIL),
            data.LOGIN_PASSWORD,
            id='6_login_with_incorrect_email'
        ),
        pytest.param(
            data.LOGIN_EMAIL,
            utilities.generate_random_string(size=randint(8, 20),
                                             punc=True,
                                             original=data.LOGIN_PASSWORD),
            id='7_login_with_incorrect_password'
        ),
        pytest.param(
            data.LOGIN_EMAIL,
            data.LOGIN_PASSWORD.swapcase(),
            id='8_login_with_case_changed_password'
        ),
    ]
)
def testing_with_incorrect_data(browser,
                                user_name,
                                pass_word):
    login_page = LoginPage(browser)
    login_page.load(url=data.LOGIN_URL)
    login_page.fill_username(user_name)
    login_page.fill_password(pass_word)
    login_page.click_login()
    login_message_has_part = login_page.check_login_message('Please try again')

    assert login_message_has_part is True
