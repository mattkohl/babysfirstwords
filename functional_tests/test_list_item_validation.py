from unittest import skip
from selenium.webdriver.common.keys import Keys
from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    @skip
    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)

        self.assertEqual(
            self.browser.find_element_by_css_selector(".has-error").text,  
            "You can't have an empty list item"  
        )

        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))
        
        self.browser.find_element_by_id("id_new_item").send_keys("Dada")
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Dada")

        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector(".has-error").text,
            "You cannot have an empty list item"
        ))

        self.browser.find_element_by_id("id_new_item").send_keys("Mama")
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Dada")
        self.wait_for_row_in_list_table("2: Mama")
