from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)
        self.assertIn("Baby's First Words", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("Start a new list", header_text)

        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a word")

        inputbox.send_keys("Dada")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Dada")

        inputbox = self.get_item_input_box()
        inputbox.send_keys("Mama")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("2: Mama")
        self.wait_for_row_in_list_table("1: Dada")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Dada")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Dada")

        first_list_url = self.browser.current_url
        self.assertRegex(first_list_url, '/lists/.+')

        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Dada", page_text)

        inputbox = self.get_item_input_box()
        inputbox.send_keys("Boo")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Boo")

        second_list_url = self.browser.current_url
        self.assertRegex(second_list_url, '/lists/.+')
        self.assertNotEqual(first_list_url, second_list_url)

        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Dada", page_text)
        self.assertIn("Boo", page_text)