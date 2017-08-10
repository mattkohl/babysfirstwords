from unittest import skip
from selenium import webdriver
from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage


def quit_if_possible(browser):
    try:
        browser.quit()
    except Exception as e:
        pass


class SharingTest(FunctionalTest):

    def test_can_share_a_list_with_another_user(self):
        # User is a logged-in user
        self.create_pre_authenticated_session("user@example.com")
        user_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(user_browser))

        # Friend is also on the lists site
        friend_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(friend_browser))
        self.browser = friend_browser
        self.create_pre_authenticated_session("your-friend@example.com")

        # User goes to the home page and starts a list
        self.browser = user_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item("first word")

        # User notices a "Share this list" option
        share_box = list_page.get_share_box()
        self.assertEqual(share_box.get_attribute("placeholder"), "your-friend@example.com")

        # User shares the list
        list_page.share_list_with("your-friend@example.com")

        self.browser = friend_browser
        MyListsPage(self).go_to_my_lists_page()

        # Friend sees User list there!
        self.browser.find_element_by_link_text("first word").click()
        self.wait_for(lambda: self.assertEqual(list_page.get_list_owner(), "user@example.com"))
    
        # He adds an item to the list
        list_page.add_list_item("Friend!")
    
        # When User refreshes the page, sees addition from Friend
        self.browser = user_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table("Friend!", 2)
