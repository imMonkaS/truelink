"""
Django Tests inherited from TestCase
"""

from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse

from main.models import Message


class UserTestCase(TestCase):
    """
    User page tests

    :param fixtures: - project's fixtures
    """

    fixtures = ['test_database.json']

    def setUp(self) -> None:
        """
        Class set up for tests
        """

        self.client = Client()
        self.user = User.objects.get(username='dan')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('user', kwargs={'user_id': self.user.id}))

    def test_response(self):
        """
        Tests response's status code
        """

        self.assertEqual(self.response.status_code, 200)

    def test_context_user_is_user(self):
        """
        Tests that user field in context equals to current User object
        """

        self.assertEqual(self.response.context['user'], self.user)

    def test_user_on_page(self):
        """
        Tests that user_on_page field in context equals to current user by user_id in url
        """

        self.assertEqual(self.response.context['user_on_page'], self.user)

    def test_posts_len(self):
        """
        Tests amount of posts on user's page
        """

        self.assertEqual(len(self.response.context['posts']), 0)


class GalleryTestCase(TestCase):
    """
    gallery page tests

    :param fixtures: - project's fixtures
    """

    fixtures = ['test_database.json']

    def setUp(self) -> None:
        """
        Class set up for tests
        """

        self.client = Client()
        self.user = User.objects.get(username='dan')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('gallery', kwargs={'user_id': self.user.id}))

    def test_response(self):
        """
        Tests response's status code
        """

        self.assertEqual(self.response.status_code, 200)

    def test_context_user_is_user(self):
        """
        Tests that user field in context equals to current User object
        """

        self.assertEqual(self.response.context['user'], self.user)

    def test_user_on_page(self):
        """
        Tests that user_on_page field in context equals to current user by user_id in url
        """

        self.assertEqual(self.response.context['user_on_page'], self.user)


class ProfileSettingsTestCase(TestCase):
    """
    User profile settings page tests

    :param fixtures: - project's fixtures
    """

    fixtures = ['test_database.json']

    def setUp(self) -> None:
        """
        Class set up for tests
        """

        self.client = Client()
        self.user = User.objects.get(username='dan')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('profile', kwargs={'user_id': self.user.id}))

    def test_response(self):
        """
        Tests response's status code
        """

        self.assertEqual(self.response.status_code, 200)

    def test_context_user_is_user(self):
        """
        Tests that user field in context equals to current User object
        """

        self.assertEqual(self.response.context['user'], self.user)


class PrivateSettingsTestCase(TestCase):
    """
    User private settings page test

    :param fixtures: - project's fixtures
    """

    fixtures = ['test_database.json']

    def setUp(self) -> None:
        """
        Class set up for tests
        """

        self.client = Client()
        self.user = User.objects.get(username='dan')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('private', kwargs={'user_id': self.user.id}))

    def test_response(self):
        """
        Tests response's status code
        """

        self.assertEqual(self.response.status_code, 200)

    def test_context_user_is_user(self):
        """
        Tests that user field in context equals to current User object
        """

        self.assertEqual(self.response.context['user'], self.user)

    def test_friends_visibility(self):
        """
        Tests that friends_visibility field is not None
        """

        self.assertNotEqual(self.response.context['user'].profile.friends_visible, None)

    def test_groups_visibility(self):
        """
        Tests that groups_visibility field is not None
        """

        self.assertNotEqual(self.response.context['user'].profile.groups_visible, None)

    def test_age_visibility(self):
        """
        Tests that age_visibility field is not None
        """

        self.assertNotEqual(self.response.context['user'].profile.age_visible, None)

    def test_last_name_visibility(self):
        """
        Tests that last_name_visibility field is not None
        """

        self.assertNotEqual(self.response.context['user'].profile.last_name_visible, None)


class GroupsTestCase(TestCase):
    """
    User groups page tests

    :param fixtures: - project's fixtures
    """

    fixtures = ['test_database.json']

    def setUp(self) -> None:
        """
        Class set up for tests
        """

        self.client = Client()
        self.user = User.objects.get(username='dan')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('groups', kwargs={'user_id': self.user.id}))

    def test_response(self):
        """
        Tests response's status code
        """

        self.assertEqual(self.response.status_code, 200)

    def test_context_user_is_user(self):
        """
        Tests that user field in context equals to current User object
        """

        self.assertEqual(self.response.context['user'], self.user)

    def test_user_on_page(self):
        """
        Tests that user_on_page field in context equals to current user by user_id in url
        """

        self.assertEqual(self.response.context['user_on_page'], self.user)


class FriendsTestCase(TestCase):
    """
    User friends page tests

    :param fixtures: - project's fixtures
    """

    fixtures = ['test_database.json']

    def setUp(self) -> None:
        """
        Class set up for tests
        """

        self.client = Client()
        self.user = User.objects.get(username='dan')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('friends', kwargs={'user_id': self.user.id}))

    def test_response(self):
        """
        Tests response's status code
        """

        self.assertEqual(self.response.status_code, 200)

    def test_context_user_is_user(self):
        """
        Tests that user field in context equals to current User object
        """

        self.assertEqual(self.response.context['user'], self.user)

    def test_user_on_page(self):
        """
        Tests that user_on_page field in context equals to current user by user_id in url
        """

        self.assertEqual(self.response.context['user_on_page'], self.user)


class ServersTestCase(TestCase):
    """
    User servers page tests

    :param fixtures: - project's fixtures
    """

    fixtures = ['test_database.json']

    def setUp(self) -> None:
        """
        Class set up for tests
        """

        self.client = Client()
        self.user = User.objects.get(username='dan')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('servers'))

    def test_response(self):
        """
        Tests response's status code
        """

        self.assertEqual(self.response.status_code, 200)

    def test_context_user_is_user(self):
        """
        Tests that user field in context equals to current User object
        """

        self.assertEqual(self.response.context['user'], self.user)


class GroupTestCase(TestCase):
    """
    Group page tests

    :param fixtures: - project's fixtures
    """

    fixtures = ['test_database.json']

    def setUp(self) -> None:
        """
        Class set up for tests
        """

        self.client = Client()
        self.user = User.objects.get(username='dan')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('group', kwargs={'group_id': 1}))

    def test_response(self):
        """
        Tests response's status code
        """

        self.assertEqual(self.response.status_code, 200)

    def test_context_user_is_user(self):
        """
        Tests that user field in context equals to current User object
        """

        self.assertEqual(self.response.context['user'], self.user)


class GroupMembersTestCase(TestCase):
    """
    Group members page tests

    :param fixtures: - project's fixtures
    """

    fixtures = ['test_database.json']

    def setUp(self) -> None:
        """
        Class set up for tests
        """

        self.client = Client()
        self.user = User.objects.get(username='dan')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('group_members', kwargs={'group_id': 1}))

    def test_response(self):
        """
        Tests response's status code
        """

        self.assertEqual(self.response.status_code, 200)

    def test_context_user_is_user(self):
        """
        Tests that user field in context equals to current User object
        """

        self.assertEqual(self.response.context['user'], self.user)

    def test_members(self):
        """
        Tests that there is at least one user in members
        """

        self.assertNotEqual(len(self.response.context['members']), 0)


class ServerTestCase(TestCase):
    """
    Server page tests

    :param fixtures: - project's fixtures
    """

    fixtures = ['test_database.json']

    def setUp(self) -> None:
        """
        Class set up for tests
        """

        self.client = Client()
        self.user = User.objects.get(username='dan')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('server', kwargs={'server_id': 1}) + '?chat=1')

    def test_response(self):
        """
        Tests response's status code
        """

        self.assertEqual(self.response.status_code, 200)

    def test_context_user_is_user(self):
        """
        Tests that user field in context equals to current User object
        """

        self.assertEqual(self.response.context['user'], self.user)


class ServerMembersTestCase(TestCase):
    """
    Server members page tests

    :param fixtures: - project's fixtures
    """

    fixtures = ['test_database.json']

    def setUp(self) -> None:
        """
        Class set up for tests
        """

        self.client = Client()
        self.user = User.objects.get(username='dan')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('server_members', kwargs={'server_id': 1}))

    def test_response(self):
        """
        Tests response's status code
        """

        self.assertEqual(self.response.status_code, 200)

    def test_context_user_is_user(self):
        """
        Tests that user field in context equals to current User object
        """

        self.assertEqual(self.response.context['user'], self.user)

    def test_members(self):
        """
        Tests that there is at least one user in members
        """

        self.assertNotEqual(len(self.response.context['members']), 0)


class NewGroupTestCase(TestCase):
    """
    Create new group page tests

    :param fixtures: - project's fixtures
    """

    fixtures = ['test_database.json']

    def setUp(self) -> None:
        """
        Class set up for tests
        """

        self.client = Client()
        self.user = User.objects.get(username='dan')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('new_group'))

    def test_response(self):
        """
        Tests response's status code
        """

        self.assertEqual(self.response.status_code, 200)

    def test_context_user_is_user(self):
        """
        Tests that user field in context equals to current User object
        """

        self.assertEqual(self.response.context['user'], self.user)


class NewServerTestCase(TestCase):
    """
    Create new server page tests

    :param fixtures: - project's fixtures
    """

    fixtures = ['test_database.json']

    def setUp(self) -> None:
        """
        Class set up for tests
        """

        self.client = Client()
        self.user = User.objects.get(username='dan')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('new_server'))

    def test_response(self):
        """
        Tests response's status code
        """

        self.assertEqual(self.response.status_code, 200)

    def test_context_user_is_user(self):
        """
        Tests that user field in context equals to current User object
        """

        self.assertEqual(self.response.context['user'], self.user)


class SearchTestCase(TestCase):
    """
    Search page tests

    :param fixtures: - project's fixtures
    """

    fixtures = ['test_database.json']

    def setUp(self) -> None:
        """
        Class set up for tests
        """

        self.client = Client()
        self.user = User.objects.get(username='dan')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('search') + '?search=sth')

    def test_response(self):
        """
        Tests response's status code
        """

        self.assertEqual(self.response.status_code, 200)

    def test_context_user_is_user(self):
        """
        Tests that user field in context equals to current User object
        """

        self.assertEqual(self.response.context['user'], self.user)
