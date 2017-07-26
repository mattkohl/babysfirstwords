from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):

        # Go to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1440, 900)

        # the input box is centered
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(inputbox.location["x"] + inputbox.size["width"] / 2, 672, delta=10)
        inputbox.send_keys("testing")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: testing")

        # Start a new list and that input is centered as well
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(inputbox.location["x"] + inputbox.size["width"] / 2, 672, delta=10)