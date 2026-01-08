import unittest

from selenium import webdriver


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_todo_list(self):
        # user wants to use the Todo app
        self.browser.get("http://localhost:8000")

        # user sees the title
        self.assertIn("To-Do", self.browser.title)

        # user sees a box to enter todos
        self.fail("Finish the test!")
        # user enters "buy milk" in the box

        # user sees page refresh, list contains "buy milk"

        # user enters "drink milk" in the box

        # user sees page refresh, list contains both todo items"

        # user quits.

if __name__ == "__main__":
    unittest.main()
