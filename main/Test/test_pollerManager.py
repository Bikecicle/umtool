from unittest import TestCase
from db.DatabaseMisc import DatabaseMisc
from model.PollerManager import PollerManager
from model.Job import Job
from model.Job import Host
import time

class TestPollerManager(TestCase):

    def test_check_database_state(self):
        # Set up
        db = MockDB()
        poller_manager = PollerManager("pm1")
        poller_manager.db = db
        job_1 = Job("j1", 1, [Host("hostname", "user", "pass", "unique")])
        job_2 = Job("j2", 1, [Host("hostname", "user", "pass", "unique")])

        # Start a job and check state
        db.create_job(job_1, poller_manager.spawner_id)
        poller_manager.check_database_state()
        self.assertIn("j1", poller_manager.pollers)
        self.assertIsNotNone(poller_manager.pollers["j1"])
        self.assertFalse(poller_manager.pollers["j1"].stopped)

        # Start and check another one
        db.create_job(job_2, poller_manager.spawner_id)
        poller_manager.check_database_state()
        self.assertIn("j2", poller_manager.pollers)
        self.assertIsNotNone(poller_manager.pollers["j2"])
        self.assertFalse(poller_manager.pollers["j2"].stopped)

        # Send kill command and check state
        db.kill_job("j1")
        poller_manager.check_database_state()
        self.assertTrue(poller_manager.pollers["j1"].stopped)
        self.assertTrue(db.check_if_job_is_fully_dead("j1"))

class MockDB:

    def __init__(self):
        self.jobs = []
        self.kill = []
        self.dead = []

    def create_job(self, job, spawner_id):
        self.jobs.append(job)

    def kill_job(self, job_id):
        self.kill.append(job_id)

    def check_job_assignments(self, spawner_id):
        return self.jobs

    def check_kill_order(self, job_id):
        return job_id in self.kill

    def spawner_report_death_complete(self, job_id, spawner_id):
        self.dead = job_id

    def check_if_job_is_fully_dead(self, job_id):
        return job_id in self.dead
