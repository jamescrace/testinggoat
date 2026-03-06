import os
import time
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

MAX_WAIT = 5


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        options = Options()
        options.add_argument("-headless")
        self.browser = webdriver.Firefox(options=options)
        if test_server := os.environ.get("TEST_SERVER"):
            self.live_server_url = "https://" + test_server

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            from selenium.common import WebDriverException
            try:
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)

    def get_item_input_box(self):
        return self.browser.find_element(By.ID, "id_text")
