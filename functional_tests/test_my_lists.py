from django.conf import settings
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        # to set a cookie we need to first visit the domain. 404 pages load the quickest!
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path="/",
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Start with a logged-in user
        self.create_pre_authenticated_session("user@example.com")

        # User goes to the home page and starts a list
        self.browser.get(self.live_server_url)
        self.add_list_item("trucks")
        self.add_list_item("boats")

        # User notices a "My lists" link, for the first time.
        self.browser.find_element_by_link_text("My lists").click()

        # User sees list is in there, named according to its first list item
        self.wait_for(
            lambda: self.browser.find_element_by_link_text("trucks")
        )
        self.browser.find_element_by_link_text("trucks").click()

        # User decides to start another list, just to see
        self.browser.get(self.live_server_url)
        self.browser.get(self.live_server_url)
        self.add_list_item("cows")
        self.add_list_item("horses")
        self.add_list_item("ducks")

        # Under "my lists", the new list appears
        self.browser.find_element_by_link_text("My lists").click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text("cows")
        )
        self.browser.find_element_by_link_text("cows").click()

