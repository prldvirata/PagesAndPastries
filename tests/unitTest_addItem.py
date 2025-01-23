# Selenium test script
# test script to verify a valid user is logged out successfully
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

import warnings


class ll_ATS(unittest.TestCase):
    # set up the test class - assign the driver to Chrome - if using a different
    # browser, change the browser name below
    def setUp(self):
        self.driver = webdriver.Chrome()
        warnings.simplefilter('ignore', ResourceWarning)  # ignore resource warning if occurs

    # If login is successful, 'Logout' will be displayed as the text in the Navbar
    def test_ll(self):
        user = "pvirata"  # must be a valid username for the application
        pwd = "cookies99!"  # must be the password for a valid user
        name = "testing"
        prc = "2"

        driver = self.driver
        driver.maximize_window()
        driver.get("https://pvirata.pythonanywhere.com/admin")

        elem = driver.find_element(By.ID, "id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID, "id_password")
        elem.send_keys(pwd)
        time.sleep(5)
        elem.send_keys(Keys.RETURN)
        driver.get("https://pvirata.pythonanywhere.com")
        time.sleep(5)

        driver.find_element(By.XPATH, "//a[contains(., 'Add Item')]").click()
        time.sleep(5)
        select = Select(driver.find_element(By.ID, "id_category"))
        select.select_by_value('1')
        elem = driver.find_element(By.ID, "id_name")
        elem.send_keys(name)
        elem = driver.find_element(By.ID, "id_slug")
        elem.send_keys(name)
        elem = driver.find_element(By.ID, "id_price")
        elem.send_keys(prc)
        elem.send_keys(Keys.RETURN)
        time.sleep(10)

        def tearDown(self):
            self.driver.quit()


if __name__ == "__main__":
    unittest.main(warnings='ignore')