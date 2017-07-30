from unittest import skip
from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest

TEST_EMAIL = "user@example.com"
SUBJECT = "Your login link for Baby's First Words"


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):

        # Go to site and enter email address
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name("email").send_keys(TEST_EMAIL)
        self.browser.find_element_by_name("email").send_keys(Keys.ENTER)

        # A message appears indicating an email has been sent
        self.wait_for(lambda: self.assertIn(
            "Check your email",
            self.browser.find_element_by_tag_name("body").text
        ))

        # Checks email to find a message
        email = mail.outbox[0]  
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # Message has a url link in it
        self.assertIn("Use this link to log in", email.body)
        url_search = re.search(r"https?://.+/.+$", email.body)
        if not url_search:
            self.fail("Could not find url in email body:\n{}".format(email.body))
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # she clicks it
        self.browser.get(url)

        # she is logged in!
        self.wait_for(
            lambda: self.browser.find_element_by_link_text("Log out")
        )
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertIn(TEST_EMAIL, navbar.text)
