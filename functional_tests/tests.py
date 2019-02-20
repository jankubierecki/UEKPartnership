import sys
import time

from authorization.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver


class BaseConfiguration(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(self):
        for arg in sys.argv:
            if 'liveserver' in arg:
                self.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        self.server_url = self.live_server_url

    @classmethod
    def tearDownClass(self):
        if self.server_url == self.live_server_url:
            super().tearDownClass()

    def setUp(self):

        self.user = User.objects.create_superuser(email="test@test.com", password="test")

        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def submit_login_form(self, email=None, password=None):

        self.browser.get(self.server_url)

        email_field = self.browser.find_element_by_name('username')
        password_field = self.browser.find_element_by_name('password')

        if email and password:
            email_field.send_keys(email)
            password_field.send_keys(password)

        submit = 'input[type="submit"]'
        submit = self.browser.find_element_by_css_selector(submit)
        submit.click()


class LoingPageErrorTest(BaseConfiguration):

    def test_login_error(self):
        self.submit_login_form('test', 'test')

        error_note = self.browser.find_element_by_class_name('errornote')

        self.assertTrue(error_note.is_displayed())
        self.assertFalse(error_note.is_selected())
        self.assertIn('Wprowadź poprawne dane w polach', error_note.text)
        self.assertAlmostEqual(error_note.size['width'], 350, delta=5)
        self.assertAlmostEqual(error_note.size['height'], 80, delta=5)
        self.assertEqual(error_note.tag_name, 'p')

        email_field = self.browser.find_element_by_name('username')
        password_field = self.browser.find_element_by_name('password')

        email_field.clear()
        password_field.clear()

        submit = 'input[type="submit"]'
        submit = self.browser.find_element_by_css_selector(submit)
        submit.click()

        error_note = self.browser.find_element_by_class_name('errornote')

        self.assertTrue(error_note.is_displayed())


class MainPageTest(BaseConfiguration):

    def test_main_page(self):

        self.submit_login_form(email="test@test.com", password="test")

        user_board = self.browser.find_element_by_id('user-tools')
        user_board_name = user_board.find_element_by_xpath('//strong').text

        self.assertEqual(user_board_name, 'TEST@TEST.COM')

        time.sleep(5)