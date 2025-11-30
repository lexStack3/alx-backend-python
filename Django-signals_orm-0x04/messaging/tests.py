from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification


User = get_user_model()


class TestMessageModel(TestCase):
    """
    Testcase for Message model.
    """

    @classmethod
    def setUpClass(cls):
        cls.lex = User.objects.create(
            username='lex',
            email='lex@mail.com',
            first_name='Alexander',
            last_name='Edim',
            password='lexpassword'
        )

        cls.marve = User.objects.create(
            username='marve',
            email='marve@mail',
            first_name='Marvellous',
            last_name='Ocha',
            password='marvepassword'
        )

    @classmethod
    def tearDownClass(cls):
        cls.lex.delete()
        cls.marve.delete()


    def test_message_creation_creates_notification(self):
        """
        Testing singals for notification.
        """
        message = Message.objects.create(
            sender=self.lex,
            receiver=self.marve,
            content="Hi Marve!"
        )

        self.assertEqual(Message.objects.count(), 1)
        notification = Notification.objects.get(message=message)
        self.assertEqual(notification.sender, self.lex)
        self.assertFalse(notification.read)

    def test_message_reverse_relationships(self):
        """
        Testing reverse relationships on <user> instance.
        """
        m1 = Message.objects.create(
            sender=self.lex, receiver=self.marve,
            content="Hi Marve"
        )
        m2 = Message.objects.create(
            sender=self.marve, receiver=self.lex,
            content="Hello lex, how do you do?"
        )
        self.assertIn(m1, self.lex.sent_messages.all())
        self.assertIn(m2, self.lex.received_messages.all())
        self.assertIn(m2, self.marve.sent_messages.all())
        self.assertIn(m1, self.marve.received_messages.all())

    def text_notification_str_method(self):
        """
        Testing the string representation of a <Notification> instance.
        """
        message = Message.objects.create(
            sender=self.lex, receiver=self.marve,
            content="Hello Marve"
        )
        notification = Notification.objects.get(message=message)
        expected_str = "Notif from {}: {}".format(
            self.lex.username, message.content[:20]
        )

        self.assertEqual(str(notification), expected_str)

    def test_message_str_method(self):
        """
        Testing the string representation of a <Message> instance.
        """
        message = Message.objects.create(
            sender=self.lex, receiver=self.marve,
            content="Yo! How you doing?"
        )
        expected_str = "Message {}: {} to {}".format(
            message.message_id, self.lex.username,
            self.marve.username
        )

        self.assertEqual(str(message), expected_str)
