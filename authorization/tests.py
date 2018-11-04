import base64

from django.contrib.auth.models import Group, Permission
from django.test import TestCase

from authorization.models import User


class UserAccessAuthenticationTestCase(TestCase):
    """ base user test authentication via http """

    def setUp(self):
        self.credentials = base64.b64encode(b'email:password').decode("ascii")
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Basic ' + self.credentials

        self.user = User.objects.create_user(email='test@test.com', password='test')
        self.user.is_staff = True

    def test_authorized(self):
        """ tests if commissioned user can access """

        can_add_company_permission = Permission.objects.get(name='Can add Firma')

        self.user.user_permissions.add(can_add_company_permission)
        self.user.save()

        self.client.force_login(self.user, backend=None)

        response = self.client.get('/company/company/add/')
        self.assertEqual(response.status_code, 200)

    def test_not_authorized(self):
        """ tests if not authorized user can access """

        self.client.force_login(self.user, backend=None)

        response = self.client.get('/company/company/add/')
        self.assertEqual(response.status_code, 302)

    def test_is_not_staff_access(self):
        """ tests if user that is not in staff can have access """

        self.user.is_staff = False

        can_add_company_permission = Permission.objects.get(name='Can add Firma')
        self.user.user_permissions.add(can_add_company_permission)
        self.user.save()

        self.client.force_login(self.user, backend=None)

        response = self.client.get('/company/company/add/')
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        Group.objects.all().delete()
        User.objects.all().delete()


class GroupTestCase(TestCase):
    """ test user group permissions """

    def setUp(self):
        self.credentials = base64.b64encode(b'email:password').decode("ascii")
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Basic ' + self.credentials
        self.group = Group(name='test')
        self.group.save()
        self.group.permissions.add(Permission.objects.get(name='Can add Firma'))
        self.user = User.objects.create_user(email="test@example.com", password="test")
        self.user.is_staff = True

    def test_user_can_access(self):
        """ tests if user with new group can access """

        self.user.groups.add(self.group)
        self.user.save()

        self.client.force_login(self.user, backend=None)
        response = self.client.get('/company/company/add/')
        self.assertEqual(response.status_code, 200, u'user in group should have access')

    def test_user_cannot_access(self):
        """ tests if user without group cannot access """

        self.user.save()

        self.client.force_login(self.user, backend=None)
        response = self.client.get('/company/company/add/')
        self.assertEqual(response.status_code, 403, u'user not in group should have not access')

    def tearDown(self):
        Group.objects.all().delete()
        User.objects.all().delete()
