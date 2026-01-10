import time
import unittest

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_todo_list(self):
        # user wants to use the Todo app
        self.browser.get("http://localhost:8000")

        # user notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # user is invited to enter a to-do item straight away
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(
            inputbox.get_attribute("placeholder"), "Enter a to-do item"
        )
        # user enters "buy milk" in the box
        inputbox.send_keys("buy milk")

        # user sees page refresh, list contains "buy milk"
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table("1: buy milk")

        # user enters "drink milk" in the box
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("drink milk")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # user sees page refresh, list contains both todo items"
        self.check_for_row_in_list_table("2: drink milk")
        self.check_for_row_in_list_table("1: buy milk")

        # user quits.


if __name__ == "__main__":
    unittest.main()
