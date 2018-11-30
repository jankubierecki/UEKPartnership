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

        User.objects.create_superuser(email="test@test.com", password="test")

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
        self.browser.get('{}{}'.format(self.server_url, '/company/company'))

        self.submit_login_form('test', 'test')

        error_note = self.browser.find_element_by_class_name('errornote')

        self.assertTrue(error_note.is_displayed())
        self.assertFalse(error_note.is_selected())

        self.assertIn('Wprowadź poprawne dane w polach', error_note.text)

        self.assertAlmostEqual(error_note.size['width'], 350, delta=5)
        self.assertAlmostEqual(error_note.size['height'], 80, delta=5)

        self.assertEqual(error_note.tag_name, 'p')


class MainPageTest(BaseConfiguration):
    pass
