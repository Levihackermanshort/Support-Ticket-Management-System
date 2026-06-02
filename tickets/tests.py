from django.test import TestCase
from django.contrib.auth import get_user_model
from tickets.models import Ticket, Reply


User = get_user_model()


class TicketModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass')

    def test_ticket_creation_and_str(self):
        t = Ticket.objects.create(subject='Hello world', description='desc', created_by=self.user)
        self.assertIn('Hello', str(t))

    def test_reply_prevent_on_closed(self):
        t = Ticket.objects.create(subject='T', description='d', created_by=self.user, status=Ticket.STATUS_CLOSED)
        r = Reply(ticket=t, user=self.user, message='hi')
        with self.assertRaises(Exception):
            r.full_clean()
