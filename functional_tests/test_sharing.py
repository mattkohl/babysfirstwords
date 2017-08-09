from unittest import skip
from selenium import webdriver
from .base import FunctionalTest
from .list_page import ListPage


def quit_if_possible(browser):
    try:
        browser.quit()
    except Exception as e:
        pass


class SharingTest(FunctionalTest):

    @skip
    def test_can_share_a_list_with_another_user(self):
        # User is a logged-in user
        self.create_pre_authenticated_session("user@example.com")
        user_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(user_browser))

        # User"s friend is also on the lists site
        oni_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.browser = oni_browser
        self.create_pre_authenticated_session("user_1@example.com")

        # User goes to the home page and starts a list
        self.browser = user_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item("first word")

        # User notices a "Share this list" option
        share_box = self.browser.find_element_by_css_selector('input[name="sharee"]')
        self.assertEqual(share_box.get_attribute("placeholder"),"your-friend@example.com")

        # User shares the list
        list_page.share_list_with("your-friend@example.com")