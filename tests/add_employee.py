import time
from random import randint
import pytest
from selenium import webdriver
from data.data import Data
from pages.login import LoginPage
from pages.dashboard import DashboardPage
from pages.staff import StaffPage
from pages.add_employee import AddEmployeesPage, AddEmployeesResultPage
import utilities

data = Data


@pytest.fixture
def browser():
    driver = webdriver.Chrome(data.CHROME_DRIVER_PATH)
    driver.maximize_window()
    yield driver
    driver.quit()


def start_page(browser):
    login_page = LoginPage(browser)
    login_page.load(url=data.LOGIN_URL)
    login_page.fill_username(data.LOGIN_EMAIL)
    login_page.fill_password(data.LOGIN_PASSWORD)
    login_page.click_login()
    time.sleep(3)
    dashboard_page = DashboardPage(browser)
    dashboard_page.click_staff()
    time.sleep(3)
    staff_page = StaffPage(browser)
    staff_page.click_add_employee()
    time.sleep(3)
    add_employees_page = AddEmployeesPage(browser)

    return add_employees_page


def test_add_employee(browser):
    page = start_page(browser)
    ordinal_num = page.choose_ordinal_number()

    first_name = utilities.generate_random_string(size=randint(6, 30))
    last_name = utilities.generate_random_string(size=randint(6, 30))

    page.fill_field(text=first_name,
                    ordinal_number=ordinal_num,
                    part_of_locator=page.INPUT_FIRST_NAME)
    page.fill_field(text=last_name,
                    ordinal_number=ordinal_num,
                    part_of_locator=page.INPUT_LAST_NAME)
    page.fill_field(text=utilities.generate_random_email(data.LOGIN_EMAIL),
                    ordinal_number=ordinal_num,
                    part_of_locator=page.INPUT_EMAIL)
    page.click_save()

    time.sleep(5)

    result_page = AddEmployeesResultPage(browser)
    results = result_page.check_results([f'{first_name} {last_name}'])

    assert results is True


def test_add_employees(browser):
    page = start_page(browser)
    number_of_populated_rows = randint(2, page.MAX_ROWS)
    list_of_names = []

    for row in range(1, number_of_populated_rows + 1):
        first_name = utilities.generate_random_string(randint(5, 25))
        last_name = utilities.generate_random_string(randint(5, 35))
        list_of_names.append(f'{first_name} {last_name}')

        page.fill_field(text=first_name,
                        ordinal_number=row,
                        part_of_locator=page.INPUT_FIRST_NAME)
        page.fill_field(text=last_name,
                        ordinal_number=row,
                        part_of_locator=page.INPUT_LAST_NAME)
        page.fill_field(text=f'{first_name.lower()}.{last_name.lower()}@{data.DOMAIN}',
                        ordinal_number=row,
                        part_of_locator=page.INPUT_EMAIL)

    page.click_save()
    time.sleep(5)

    result_page = AddEmployeesResultPage(browser)
    results = result_page.check_results(list_of_names)

    assert results is True


def test_all_empty_values(browser):
    page = start_page(browser)
    page.click_save()
    status_message_has_text = page.check_status_message(page.STATUS_ALL_EMPTY)

    assert status_message_has_text is True


def test_empty_first_name(browser):
    page = start_page(browser)
    ordinal_num = page.choose_ordinal_number()

    page.fill_field(text=utilities.generate_random_string(),
                    ordinal_number=ordinal_num,
                    part_of_locator=page.INPUT_LAST_NAME)
    page.fill_field(text=utilities.generate_random_email(data.LOGIN_EMAIL),
                    ordinal_number=ordinal_num,
                    part_of_locator=page.INPUT_EMAIL)
    page.click_save()
    status_message_has_text = page.check_status_message(page.STATUS_MANDATORY_FIELD)

    assert status_message_has_text is True


def test_incorrect_email(browser):
    page = start_page(browser)
    ordinal_num = page.choose_ordinal_number()

    page.fill_field(text=utilities.generate_random_string(size=randint(10, 60)),
                    ordinal_number=ordinal_num,
                    part_of_locator=page.INPUT_FIRST_NAME)
    page.fill_field(text=utilities.generate_random_string(size=randint(8, 30)),
                    ordinal_number=ordinal_num,
                    part_of_locator=page.INPUT_LAST_NAME)
    page.fill_field(text=utilities.generate_random_string(size=randint(3, 50), punc=True),
                    ordinal_number=ordinal_num,
                    part_of_locator=page.INPUT_EMAIL)
    page.click_save()
    status_message_has_text = page.check_status_message(page.STATUS_INCORRECT_EMAIL)

    assert status_message_has_text is True


def test_empty_first_name_employees(browser):
    page = start_page(browser)
    number_of_populated_rows = randint(2, page.MAX_ROWS)
    row_with_empty_first_name = randint(1, number_of_populated_rows)

    for row in range(1, number_of_populated_rows + 1):
        first_name = utilities.generate_random_string(size=randint(10, 50))
        last_name = utilities.generate_random_string(size=randint(10, 80))

        if row != row_with_empty_first_name:
            page.fill_field(text=first_name,
                            ordinal_number=row,
                            part_of_locator=page.INPUT_FIRST_NAME)

        page.fill_field(text=last_name,
                        ordinal_number=row,
                        part_of_locator=page.INPUT_LAST_NAME)
        page.fill_field(text=f'{first_name.lower()}.{last_name.lower()}@{data.DOMAIN}',
                        ordinal_number=row,
                        part_of_locator=page.INPUT_EMAIL)

    page.click_save()

    status_message_has_text = page.check_status_message(page.STATUS_MANDATORY_FIELD)

    assert status_message_has_text is True


def test_incorrect_email_employees(browser):
    page = start_page(browser)
    number_of_populated_rows = randint(2, page.MAX_ROWS)
    row_with_incorrect_email = randint(1, number_of_populated_rows)

    for row in range(1, number_of_populated_rows + 1):
        first_name = utilities.generate_random_string()
        last_name = utilities.generate_random_string()

        page.fill_field(text=first_name,
                        ordinal_number=row,
                        part_of_locator=page.INPUT_FIRST_NAME)
        page.fill_field(text=last_name,
                        ordinal_number=row,
                        part_of_locator=page.INPUT_LAST_NAME)

        if row != row_with_incorrect_email:
            page.fill_field(text=f'{first_name.lower()}.{last_name.lower()}@{data.DOMAIN}',
                            ordinal_number=row,
                            part_of_locator=page.INPUT_EMAIL)
        else:
            page.fill_field(text=utilities.generate_random_string(size=75, punc=True),
                            ordinal_number=row,
                            part_of_locator=page.INPUT_EMAIL)

    page.click_save()

    status_message_has_text = page.check_status_message(page.STATUS_INCORRECT_EMAIL)

    assert status_message_has_text is True


def test_empty_first_name_incorrect_email_employees(browser):
    page = start_page(browser)
    num_populated_rows = randint(2, page.MAX_ROWS)
    row_empty_first_name, row_incorrect_email = randint(1, num_populated_rows), randint(1, num_populated_rows)

    for row in range(1, num_populated_rows + 1):
        first_name = utilities.generate_random_string(size=randint(5, 60))
        last_name = utilities.generate_random_string(size=randint(10, 70))

        if row != row_empty_first_name:
            page.fill_field(text=first_name,
                            ordinal_number=row,
                            part_of_locator=page.INPUT_FIRST_NAME)
        page.fill_field(text=last_name,
                        ordinal_number=row,
                        part_of_locator=page.INPUT_LAST_NAME)
        if row != row_incorrect_email:
            page.fill_field(text=f'{first_name.lower()}.{last_name.lower()}@{data.DOMAIN}',
                            ordinal_number=row,
                            part_of_locator=page.INPUT_EMAIL)
        else:
            page.fill_field(text=utilities.generate_random_string(randint(5, 40), punc=True),
                            ordinal_number=row,
                            part_of_locator=page.INPUT_EMAIL)

    page.click_save()

    status_message_has_text = False

    if row_empty_first_name <= row_incorrect_email:
        status_message_has_text = page.check_status_message(page.STATUS_MANDATORY_FIELD)
    else:
        status_message_has_text = page.check_status_message(page.STATUS_INCORRECT_EMAIL)

    assert status_message_has_text is True


def test_remove_row(browser):
    page = start_page(browser)
    ordinal_num = page.choose_ordinal_number()

    page.fill_field(text=utilities.generate_random_string(size=randint(6, 30)),
                    ordinal_number=ordinal_num,
                    part_of_locator=page.INPUT_FIRST_NAME)
    page.fill_field(text=utilities.generate_random_string(size=randint(10, 40)),
                    ordinal_number=ordinal_num,
                    part_of_locator=page.INPUT_LAST_NAME)
    page.fill_field(text=utilities.generate_random_email(data.LOGIN_EMAIL),
                    ordinal_number=ordinal_num,
                    part_of_locator=page.INPUT_EMAIL)

    page.click_remove(ordinal_num)
    empty_row = page.check_empty_row(ordinal_num)

    assert empty_row is True
