from __future__ import unicode_literals
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth.models import User
from django.test import TestCase
from django.contrib.auth.models import Group

from activity.models import Action
from activity.logic import get_action_text, get_action_html, add_action


class ActivityLogicTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_bob')
        self.user2 = User.objects.create_user(username='test_gary')

    def test_add_action(self):
        """
        Tests creation of an Action.

        Also checks 'public' and 'private' custom Queryset methods work.
        """
        Action.objects.create(
            actor=self.user,
            verb='made friends with',
            action=self.user2,
        )
        Action.objects.create(
            actor=self.user,
            verb='made friends with',
            action=self.user2,
            is_public=False,
        )

        self.assertEqual(Action.objects.all().count(), 2)
        self.assertEqual(Action.objects.private().count(), 1)
        self.assertEqual(Action.objects.public().count(), 1)

    def test_get_action_text_with_verb(self):
        """
        Tests get_action_text() with a verb, that the text output is correct.
        """
        self.action = Action.objects.create(
            actor=self.user,
            verb='joined the website'
        )

        expected = 'test_bob joined the website now'
        result = get_action_text(self.action)
        self.assertEqual(expected, result)

    def test_get_action_text_with_verb_action(self):
        """
        Tests get_action_text() with a verb and action, that the text output
        is correct.
        """
        self.action = Action.objects.create(
            actor=self.user,
            verb='made friends with',
            action=self.user2,
            timestamp=timezone.now() - timedelta(days=2)
        )

        expected = 'test_bob made friends with test_gary 2 days ago'
        result = get_action_text(self.action)
        self.assertEqual(expected, result)

    def test_get_action_text_with_verb_action_target(self):
        """
        Tests get_action_text() with a verb, action and target, that the text
        output is correct.
        """
        self.group = Group.objects.create(
            name='Some group'
        )

        self.action = Action.objects.create(
            actor=self.user,
            verb='invited',
            action=self.user2,
            target=self.group,
            timestamp=timezone.now() - timedelta(days=2)
        )

        expected = 'test_bob invited test_gary to Some group 2 days ago'
        result = get_action_text(self.action)
        self.assertEqual(expected, result)

    def test_get_action_html_with_verb(self):
        """
        Tests get_action_html() with a verb, that the html output is correct.
        """
        self.action = Action.objects.create(
            actor=self.user,
            verb='joined the website'
        )

        expected = (
            '<span class="action-actor">test_bob</span>'
            '<span class="action-verb">joined the website</span>'
            '<span class="action-timestamp">now</span>'
        )
        result = get_action_html(self.action)
        self.assertHTMLEqual(expected, result)

    def test_get_action_html_with_verb_action(self):
        """
        Tests get_action_html() with a verb and action, that the html output
        is correct.
        """
        self.action = Action.objects.create(
            actor=self.user,
            verb='made friends with',
            action=self.user2,
            timestamp=timezone.now() - timedelta(days=2)
        )

        expected = (
            '<span class="action-actor">test_bob</span>'
            '<span class="action-verb">made friends with</span>'
            '<span class="action-action">test_gary</span>'
            '<span class="action-timestamp">2 days ago</span>'
        )
        result = get_action_html(self.action).strip()
        self.assertHTMLEqual(expected, result)

    def test_get_action_html_with_verb_action_target(self):
        """
        Tests get_action_html() with a verb, action and target, that
        the html output is correct.
        """
        self.group = Group.objects.create(
            name='Some group'
        )

        self.action = Action.objects.create(
            actor=self.user,
            verb='invited',
            action=self.user2,
            target=self.group,
            timestamp=timezone.now() - timedelta(days=2)
        )
        expected = (
            '<span class="action-actor">test_bob</span>'
            '<span class="action-verb">invited</span>'
            '<span class="action-action">test_gary</span>'
            ' to '
            '<span class="action-target">Some group</span>'
            '<span class="action-timestamp">2 days ago</span>'
        )
        result = get_action_html(self.action)
        self.assertHTMLEqual(expected, result)

    def test_add_action_func(self):
        """
        Test the logic function add_action adds the Action record correctly.
        """

        add_action(
            actor=self.user,
            verb='made friends with',
            action=self.user2
        )

        action = Action.objects.all()[0]

        self.assertEqual(Action.objects.all().count(), 1)

        self.assertEqual(action.actor, self.user)
        self.assertEqual(action.verb, 'made friends with')
        self.assertEqual(action.action, self.user2)
