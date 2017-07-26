from selenium.webdriver.common.keys import Keys
from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):

        # Try to submit empty input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Browser intercepts the request, and does not load list page
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        # Start typing some text and the error disappears
        self.get_item_input_box().send_keys("Dada")
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))

        # Submit it successfully
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Dada")

        # Try to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Browser will not comply
        self.wait_for_row_in_list_table("1: Dada")
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        # Correct it by filling in some text
        self.get_item_input_box().send_keys("Mama")
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Dada")
        self.wait_for_row_in_list_table("2: Mama")

    def test_cannot_add_duplicate_items(self):

        # Go to the home page and start a new list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("Dada")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Dada")

        # Try to submit a duplicate item
        self.get_item_input_box().send_keys("Dada")
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Get an error message
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector(".has-error").text,
            "You already have this in your list"
        ))

    def test_error_messages_are_cleared_on_input(self):
        # Start a list and causes a validation error
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("Dada")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Dada")
        self.get_item_input_box().send_keys("Dada")
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.browser.find_element_by_css_selector(".has-error").is_displayed()
        ))

        # Start typing in the input box to clear the error
        self.get_item_input_box().send_keys("a")

        # The error message disappears
        self.wait_for(lambda: self.assertFalse(
            self.browser.find_element_by_css_selector(".has-error").is_displayed()
        ))