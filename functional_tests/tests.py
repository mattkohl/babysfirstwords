import os
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException


MAX_WAIT = 3


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'https://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)
        self.assertIn("Baby's First Words", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("Start a new list", header_text)
        
        inputbox = self.browser.find_element_by_id("id_new_item")  
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a word")
        
        inputbox.send_keys("Dada")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Dada")

        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Mama")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("2: Mama")
        self.wait_for_row_in_list_table("1: Dada")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id("id_new_item")
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

        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Boo")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Boo")

        second_list_url = self.browser.current_url
        self.assertRegex(second_list_url, '/lists/.+')
        self.assertNotEqual(first_list_url, second_list_url)

        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Dada", page_text)
        self.assertIn("Boo", page_text)

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=10
        )
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
