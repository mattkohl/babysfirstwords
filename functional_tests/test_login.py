import os
import poplib
import re
import time
from django.core import mail
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


SUBJECT = "Your login link for Baby's First Words"


class LoginTest(FunctionalTest):

    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL("pop.mail.yahoo.com")
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ["YAHOO_PASSWORD"])
            while time.time() - start < 60:
                # get 10 newest messages
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print("getting msg", i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode("utf8") for l in lines]
                    print(lines)
                    if "Subject: {}".format(subject) in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

    def test_can_get_email_link_to_log_in(self):
        if self.staging_server:
            test_email = os.environ.get("YAHOO_ADDRESS")
        else:
            test_email = 'user@example.com'

        # Go to site and enter email address
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name("email").send_keys(test_email)
        self.browser.find_element_by_name("email").send_keys(Keys.ENTER)

        # A message appears indicating an email has been sent
        self.wait_for(lambda: self.assertIn(
            "Check your email",
            self.browser.find_element_by_tag_name("body").text
        ))

        # Checks email to find a message
        body = self.wait_for_email(test_email, SUBJECT)

        # Message has a url link in it
        self.assertIn("Use this link to log in", body)
        url_search = re.search(r"https?://.+/.+$", body)
        if not url_search:
            self.fail("Could not find url in email body:\n{}".format(body))
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # user clicks it
        # self.browser.find_element_by_link_text('Log out').click()

        # user is logged in!
        # self.wait_to_be_logged_in(email=test_email)
