from unittest import TestCase
from model.JobManager import JobManager
from model.Job import Host
import docker


class TestJobManager(TestCase):
    def setUp(self):
        self.job_manager = JobManager()
        self.client = docker.from_env()

        self.host_list = [Host("host", "user", "pass", "unique_id")]
        self.interval = 1

    def test_start_new_spawner(self):
        # Test successful creation
        spawner_a = self.job_manager.start_new_spawner()
        self.assertIsNotNone(spawner_a)
        self.assertIn(spawner_a.container, self.client.containers.list())
        self.assertEqual(1, len(self.job_manager.spawners))
        self.assertIn("spawner_internal.py", str(spawner_a.container.top()))

        # Test multiple spawners
        spawner_b = self.job_manager.start_new_spawner()
        self.assertIsNotNone(spawner_b)
        self.assertIn(spawner_b.container, self.client.containers.list())
        self.assertEqual(2, len(self.job_manager.spawners))
        self.assertIn("spawner_internal.py", str(spawner_b.container.top()))

        self.job_manager.kill_all_spawners()

    def test_kill_spawner(self):
        spawner = self.job_manager.start_new_spawner()

        # Test invalid spawner_id
        self.assertFalse(self.job_manager.kill_spawner("invalid_spawner_id"))
        self.assertIn(spawner.container, self.client.containers.list())
        self.assertEqual(1, len(self.job_manager.spawners))

        # Test valid spawner_id
        self.assertTrue(self.job_manager.kill_spawner(spawner.spawner_id))
        self.assertNotIn(spawner.container, self.client.containers.list())
        self.assertEqual(0, len(self.job_manager.spawners))

    def test_kill_all_spawners(self):
        spawner_a = self.job_manager.start_new_spawner()
        spawner_b = self.job_manager.start_new_spawner()

        self.job_manager.kill_all_spawners()
        self.assertNotIn(spawner_a.container, self.client.containers.list())
        self.assertNotIn(spawner_b.container, self.client.containers.list())
        self.assertEqual(0, len(self.job_manager.spawners))

    def test_start_job(self):

        # Test single
        job_id_a = self.job_manager.start_job(self.host_list, self.interval)
        self.assertIsNotNone(job_id_a)
        self.assertEqual(1, len(self.job_manager.jobs))
        status_a = self.job_manager.job_status(job_id_a)
        self.assertIsNotNone(status_a)
        self.assertTrue(status_a["running"])

        job_id_b = self.job_manager.start_job(self.host_list, self.interval)
        self.assertIsNotNone(job_id_b)
        self.assertEqual(2, len(self.job_manager.jobs))
        status_b = self.job_manager.job_status(job_id_b)
        self.assertIsNotNone(status_b)
        self.assertTrue(status_b["running"])

        self.job_manager.kill_all_jobs()

    def test_kill_job(self):
        job_id = self.job_manager.start_job(self.host_list, self.interval)

        # Test invalid job_id
        self.assertFalse(self.job_manager.kill_job("invalid_job_id"))
        self.assertEqual(1, len(self.job_manager.jobs))
        status = self.job_manager.job_status(job_id)
        self.assertTrue(status["running"])

        # Test valid job_id
        self.assertTrue(self.job_manager.kill_job(job_id))
        self.assertEqual(1, len(self.job_manager.jobs))
        status = self.job_manager.job_status(job_id)
        self.assertFalse(status["running"])

    def test_kill_all_jobs(self):
        job_id_a = self.job_manager.start_job(self.host_list, self.interval)
        job_id_b = self.job_manager.start_job(self.host_list, self.interval)

        # Kill everything and check
        self.job_manager.kill_all_jobs()
        self.assertEqual(2, len(self.job_manager.jobs))
        status_dict = self.job_manager.list_jobs()
        self.assertFalse(status_dict[job_id_a]["running"])
        self.assertFalse(status_dict[job_id_b]["running"])

    def test_job_status(self):
        job_id = self.job_manager.start_job(self.host_list, self.interval)

        # Test invalid job id
        self.assertIsNone(self.job_manager.job_status("invalid_job_id"))

        # Test good job id
        status = self.job_manager.job_status(job_id)
        self.assertIsNotNone(status)
        self.assertTrue(status["running"])
        self.assertEqual(self.job_manager.jobs[job_id], status["delegates"])

        self.job_manager.kill_job(job_id)

        # Test job is dead
        status = self.job_manager.job_status(job_id)
        self.assertIsNotNone(status)
        self.assertFalse(status["running"])
        self.assertEqual(self.job_manager.jobs[job_id], status["delegates"])

    def test_list_jobs(self):
        job_id_a = self.job_manager.start_job(self.host_list, self.interval)
        job_id_b = self.job_manager.start_job(self.host_list, self.interval)

        # Test running list
        status_dict = self.job_manager.list_jobs()
        self.assertEqual(2, len(status_dict))
        self.assertTrue(status_dict[job_id_a]["running"])
        self.assertTrue(status_dict[job_id_b]["running"])
        self.assertEqual(self.job_manager.jobs[job_id_a], status_dict[job_id_a]["delegates"])
        self.assertEqual(self.job_manager.jobs[job_id_b], status_dict[job_id_b]["delegates"])

        self.job_manager.kill_all_jobs()

        # Test dead list
        status_dict = self.job_manager.list_jobs()
        self.assertEqual(2, len(status_dict))
        self.assertFalse(status_dict[job_id_a]["running"])
        self.assertFalse(status_dict[job_id_b]["running"])
        self.assertEqual(self.job_manager.jobs[job_id_a], status_dict[job_id_a]["delegates"])
        self.assertEqual(self.job_manager.jobs[job_id_b], status_dict[job_id_b]["delegates"])

    def tearDown(self):
        self.test_kill_all_spawners()
