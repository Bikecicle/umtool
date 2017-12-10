from unittest import TestCase
from db.DatabaseMisc import DatabaseMisc
from model.PollerManager import PollerManager
from model.Job import Job
from model.Job import Host
import time

class TestPollerManager(TestCase):

    def test_check_database_state(self):
        # Set up
        db = DatabaseMisc()
        poller_manager = PollerManager("pm1")
        job = Job("j1", 1, [Host("hostname", "user", "pass", "unique")])

        # Start a job and check state
        db.create_job(job, poller_manager.spawner_id)
        poller_manager.check_database_state()
        self.assertIn("j1", poller_manager.pollers)
        self.assertIsNotNone(poller_manager.pollers["j1"])
        self.assertFalse(poller_manager.pollers["j1"].stopped)

        # Send kill command and check state
        db.kill_job("j1")
        poller_manager.check_database_state()
        self.assertTrue(poller_manager.pollers["j1"].stopped)
        self.assertTrue(db.check_if_job_is_fully_dead("j1"))