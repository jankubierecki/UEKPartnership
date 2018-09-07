import base64

from django.contrib.auth.models import Group, Permission
from django.test import TestCase

from authorization.models import User


class BaseUserAccessAuthenticationTestCase(TestCase):
    """ base user test authentication via http """

    def setUp(self):
        self.credentials = base64.b64encode(b'email:password').decode("ascii")
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Basic ' + self.credentials

        self.user = User.objects.create_user(email='example@gmail.com', password='example')
        self.user.is_staff = True

    def test_authorized(self):
        """ tests if commissioned user can access """

        group = Group(name="Redaktor")
        group.save()

        can_add_company_permission = Permission.objects.get(name='Can add Firma')
        group.permissions.add(can_add_company_permission)
        group.save()

        self.user.groups.add(group)
        self.user.save()

        self.client.force_login(self.user, backend=None)

        self.response = self.client.get('/company/company/add/')
        self.assertEqual(self.response.status_code, 200)

    def test_not_authorized(self):
        """ tests if not authorized user can access """

        self.client.force_login(self.user, backend=None)

        self.response = self.client.get('/company/company/add/')
        self.assertEqual(self.response.status_code, 302)

