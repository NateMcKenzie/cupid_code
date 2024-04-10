import unittest
import sys
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


def flagParse():
    chrome = False
    headless = False
    with open('options.json', 'r') as options: 
        for line in options:
            if 'headless' in line:
                headless = 'true' in line
            if 'chrome' in line:
                chrome = 'true' in line
    return chrome, headless


class LoginTestCases(unittest.TestCase):

    def setUp(self):
        chrome, headless = flagParse()
        if not chrome:
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument('-headless')
            self.browser = webdriver.Firefox(options=options)
        else:
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument('--headless')
                options.add_argument('--disable-gpu')
            self.browser = webdriver.Chrome(options=options)

        self.browser.get('http://localhost:8000')
        self.browser.find_element(By.ID, 'login').click()
        self.addCleanup(self.browser.quit)

    def auto_login(self, email, url):
        # Navigate
        self.browser.find_element(By.ID, 'email').send_keys(email)
        self.browser.find_element(By.ID, 'password').send_keys('password')
        self.browser.find_element(By.ID, 'sign_in').click()

        # Wait until ready
        wait = WebDriverWait(self.browser, timeout=2)
        wait.until(lambda d: url in self.browser.current_url)

        # Navigate
        self.browser.find_element(By.ID, 'djHideToolBarButton').click()
        self.browser.find_element(By.ID, 'profile').click()

    def test_dater(self):
        self.auto_login('bob@cupidcode.com', '#/dater/home/1')
        inputs = self.browser.find_elements(By.TAG_NAME, 'input')

        # Test
        expected = ['Bob', 'The Builder', '1234567890',
                    '430909.36611535 4621007.2874155', 'dater1', 'bob@cupidcode.com']
        for i in range(len(expected)):
            # inputs[0] will be csrf token, so inputs will be offset by 1
            self.assertEqual(expected[i], inputs[i+1].get_attribute('value'))

    def test_cupid(self):
        self.auto_login('really@me.com', '#/cupid/home/4')
        inputs = self.browser.find_elements(By.TAG_NAME, 'input')

        # Test
        expected = ['Cupid', 'Himself', '1234124124', '20']
        for i in range(len(expected)):
            # inputs[0] will be csrf token, so inputs will be offset by 1
            self.assertEqual(expected[i], inputs[i+1].get_attribute('value'))

    def test_manager(self):
        self.auto_login('manager@cupidcode.com', '#/manager/home/5')
        inputs = self.browser.find_elements(By.TAG_NAME, 'input')

        # auto_login implicitly tests that you successfully reach homepage,
        # which is all manager needs


if __name__ == '__main__':
    unittest.main(verbosity=2)
