from django.contrib.auth.models import Group
from django.test import TestCase, Client
from authorization.models import User


class AuthorizationTestCase(TestCase):
    """ test user creation and permissions """

    def setUp(self):
        self.client = Client()
        self.user = self.create_user()

    def create_user(self):
        self.email = "user@example.com"
        self.password = User.objects.make_random_password()
        user, created = User.objects.get_or_create(email=self.email)
        user.set_password(self.password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        return user

    def test_admin(self):
        # Given
        self.assertEqual(self.client.login(email=self.email, password=self.password), True)
        admin_pages = [
            "/authorization/",
            "/auth/group/",
            "/auth/group/add/",
            "/authorization/user/",
            "/authorization/user/add/",
            "/password_change/"
        ]

        # When & Then
        for page in admin_pages:
            resp = self.client.get(page)
            if page ==  "/authorization/user/":
                self.assertTrue(False)
            self.assertEqual(resp.status_code, 200)

    def fail_user_login(self):
        self.assertEqual(self.client.login(email='user@example.net', password=self.password), True)


class GroupTestCase(TestCase):
    """ test user group permissions """

    def setUp(self):
        group_name = "example"
        self.group = Group(name=group_name)
        self.group.save()
        self.client = Client()
        self.user = User.objects.create_user(email="test@gmail.com", password="test")
        self.group.permissions.add(22)
        self.user.groups.add(self.group)
        self.email = self.user.email
        self.password = self.user.password
        self.user.is_staff = True
        self.user.is_active = True

    def tearDown(self):
        self.user.delete()
        self.group.delete()

    def test_user_cannot_access(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get("/auth/group/")
        self.assertEqual(response.status_code, 302, u'user in group should have access')

    def test_user_can_access(self):
        self.user.save()
        self.client.login(email=self.email, password=self.password)
        response = self.client.get("/company/company/24/change/")
        self.assertEqual(response.status_code, 200, u'user in group should have access')
