from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains as ac


class AddEmployeesPage:

    MAX_ROWS = 7
    DIV_STATUS = (By.ID, '_status')
    INPUT_FIRST_NAME = '_asf'
    INPUT_LAST_NAME = '_asl'
    INPUT_EMAIL = '_ase'
    IMG_DELETE = '//*[@id="_as_container"]/table/tbody/tr[ROW_NUMBER]/td[5]/img'
    BUTTON_SAVE = (By.ID, '_as_save_multiple')

    # status messages:
    STATUS_ALL_EMPTY = 'Add at least one employee'
    STATUS_MANDATORY_FIELD = 'First Name cannot be left empty'
    STATUS_INCORRECT_EMAIL = 'Invalid Email'
    STATUS_SAVED = 'Saved'

    def __init__(self,
                 browser):
        self.browser = browser

    def choose_ordinal_number(self):
        return randint(1, self.MAX_ROWS)

    def find_field(self,
                   ordinal_number,
                   part_of_locator):
        elem_locator = (By.ID, f'{part_of_locator}{ordinal_number}')

        return WebDriverWait(self.browser, 5).until(ec.visibility_of_element_located(elem_locator))

    def fill_field(self,
                   text,
                   ordinal_number,
                   part_of_locator):
        field = self.find_field(ordinal_number,
                                part_of_locator)
        field.send_keys(text)

    def check_empty_field(self,
                          ordinal_number,
                          part_of_locator):
        field = self.find_field(ordinal_number,
                                part_of_locator)
        value = field.get_attribute('value')
        return True if len(value) == 0 else False

    def check_empty_row(self,
                        ordinal_number):
        list_of_checks = [
            self.check_empty_field(ordinal_number=ordinal_number,
                                   part_of_locator=self.INPUT_FIRST_NAME),
            self.check_empty_field(ordinal_number=ordinal_number,
                                   part_of_locator=self.INPUT_LAST_NAME),
            self.check_empty_field(ordinal_number=ordinal_number,
                                   part_of_locator=self.INPUT_EMAIL)
        ]

        if False in list_of_checks:
            return False
        else:
            return True

    def click_remove(self,
                     ordinal_number):
        ac(self.browser).move_to_element(self.find_field(ordinal_number=ordinal_number,
                                                         part_of_locator=self.INPUT_EMAIL)).perform()
        elem_locator = (By.XPATH, self.IMG_DELETE.replace('ROW_NUMBER', str(ordinal_number+1)))
        WebDriverWait(self.browser, 10).\
            until(ec.visibility_of_element_located(elem_locator)).click()

    def click_save(self):
        WebDriverWait(self.browser, 1).until(ec.visibility_of_element_located(self.BUTTON_SAVE)).click()

    def check_status_message(self,
                             text):
        return WebDriverWait(self.browser, 10).until(ec.text_to_be_present_in_element(self.DIV_STATUS, text))


class AddEmployeesResultPage:

    TABLE_RESULTS = (By.CLASS_NAME, 'ResultsTable')
    CELLS_RESULT = "//table[@class='ResultsTable']//td[@class='employee ']"

    def __init__(self,
                 browser):
        self.browser = browser

    def show_result_table(self):
        table = WebDriverWait(self.browser, 60,
                              poll_frequency=5).until(ec.visibility_of_element_located(self.TABLE_RESULTS))
        if table:
            return True
        else:
            return False

    def check_results(self,
                      list_of_new_emloyees):
        show_table = self.show_result_table()
        if show_table is True:
            list_of_founded = []
            names_in_cells = ''
            cells = self.browser.find_elements(By.XPATH, self.CELLS_RESULT)

            for cell in cells:
                if len(cell.text) > 0:
                    names_in_cells += f'{cell.text}  '
            for elem in list_of_new_emloyees:
                if elem in names_in_cells:
                    list_of_founded.append(True)
                else:
                    list_of_founded.append(False)

            if (False in list_of_founded) or (len(list_of_founded) == 0):
                return False
            else:
                return True
        return False

