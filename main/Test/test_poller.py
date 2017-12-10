from unittest import TestCase
from model.Poller import Poller
from model.Job import Host
import time

class TestPoller(TestCase):
    def test_poll_servers(self):
        host_lost = [Host("hostname", "user", "pass", "unique")]
        interval = 1
        poller = Poller(host_lost, interval)
        poller.start()

        # Check if running
        self.assertTrue(poller.isAlive())
        self.assertFalse(poller.stopped)
        self.assertEqual(1, len(poller.failed_connection_list))

        poller.kill()
        time.sleep(1)

        # Check if stopped
        self.assertTrue(poller.stopped)
        self.assertFalse(poller.isAlive())