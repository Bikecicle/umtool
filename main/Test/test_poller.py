from unittest import TestCase
from model.Poller import Poller
from model.Job import Host

class TestPoller(TestCase):
    def test_poll_servers(self):
        host_lost = [Host("hostname", "user", "pass", "unique")]
        interval = 1
        poller = Poller(host_lost, interval)
        poller.start()

        # Check if running
        self.assertTrue(poller.isAlive())
        self.assertFalse(poller.stopped)

        poller.kill()

        # Check if stopped
        self.assertFalse(poller.isAlive())
        self.assertTrue(poller.stopped)