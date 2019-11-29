from random import randint
import pytest
from selenium import webdriver
from pages.login import LoginPage
import utilities


correct_email = ''
correct_password = ''
part_message = ' incorrect'


@pytest.fixture
def browser():

    driver = webdriver.Chrome('../chromedriver')
    driver.implicitly_wait(15)
    yield driver
    driver.quit()


@pytest.mark.parametrize(
    "user_name, pass_word",
    [
        pytest.param(
            correct_email,
            correct_password,
            id='1_login_with_correct_data'
        ),
        pytest.param(
            correct_email.swapcase(),
            correct_password,
            id='2_login_with_case_changed_email'
        ),
    ]
)
def testing_with_correct_data(browser,
                              user_name,
                              pass_word):

    login_page = LoginPage(browser)
    login_page.load()
    signin_message = login_page.signin(username=user_name,
                                       password=pass_word)

    assert part_message not in signin_message


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
            correct_password,
            id='4_login_with_empty_email'
        ),
        pytest.param(
            correct_email,
            '',
            id='5_login_with_empty_password'
        ),
        pytest.param(
            utilities.generate_random_email(correct_email),
            correct_password,
            id='6_login_with_incorrect_email'
        ),
        pytest.param(
            correct_email,
            utilities.generate_random_string(size=randint(8, 20),
                                             original=correct_password),
            id='7_login_with_incorrect_password'
        ),
        pytest.param(
            correct_email,
            correct_password.swapcase(),
            id='8_login_with_case_changed_password'
        ),

    ]
)
def testing_with_incorrect_data(browser,
                                user_name,
                                pass_word):

    login_page = LoginPage(browser)
    login_page.load()
    signin_message = login_page.signin(username=user_name,
                                       password=pass_word)

    assert part_message in signin_message
