from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):

        # Go to home page
        self.browser.get(self.live_server_url)

        # Page title and header mention Baby's First Words
        self.assertIn("Baby's First Words", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("Start a new list", header_text)

        # Input suggests entering a word
        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a word")

        # Enter a word
        inputbox.send_keys("Dada")

        # Submit and the word appears in a table below
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Dada")

        # Enter another word and submit
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Mama")
        inputbox.send_keys(Keys.ENTER)

        # That word appears in the table below along with the first
        self.wait_for_row_in_list_table("1: Dada")
        self.wait_for_row_in_list_table("2: Mama")

    def test_multiple_users_can_start_lists_at_different_urls(self):

        # Start a new list
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Dada")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Dada")

        # List has a unique URL
        first_list_url = self.browser.current_url
        self.assertRegex(first_list_url, '/lists/.+')

        # New user
        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

        # New blank list
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Dada", page_text)

        # Enter a word
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Boo")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Boo")

        # New list has a unique URL
        second_list_url = self.browser.current_url
        self.assertRegex(second_list_url, '/lists/.+')
        self.assertNotEqual(first_list_url, second_list_url)

        # New list only contains its own items
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Dada", page_text)
        self.assertIn("Boo", page_text)