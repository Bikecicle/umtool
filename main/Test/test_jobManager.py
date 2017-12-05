from unittest import TestCase
from main.model.JobManager import JobManager
from main.model.Job import Host
import docker


class TestJobManager(TestCase):
    def setUp(self):
        self.job_manager = JobManager()
        self.client = docker.from_env()

        self.host_list = [Host("eb2-2214-sd01ipmi.csc.ncsu.edu", "admin", "sdteam18", "cisco")]
        self.interval = 1

    def test_start_new_spawner(self):
        # Test successful creation
        spawner_a = self.job_manager.start_new_spawner()
        self.assertIsNotNone(spawner_a)
        self.assertEqual("running", spawner_a.container.status())
        self.assertEqual(1, len(self.job_manager.spawners))

        # Check if spawner is running python script internally
        if "python" not in spawner_a.container.top():
            self.fail("Spawner not running script")

        # Test multiple spawners
        spawner_b = self.job_manager.start_new_spawner()
        self.assertIsNotNone(spawner_b)
        self.assertEqual("running", spawner_b.container.status())
        self.assertEqual(2, len(self.job_manager.spawners))

        self.job_manager.kill_all_spawners()

    def test_kill_spawner(self):
        spawner = self.job_manager.start_new_spawner()

        # Test invalid spawner_id
        self.assertFalse(self.job_manager.kill_spawner("invalid_spawner_id"))
        self.assertEqual("running", spawner.container.status())
        self.assertEqual(1, len(self.job_manager.spawners))

        # Test valid spawner_id
        self.assertTrue(self.job_manager.kill_spawner(spawner.spawner_id))
        self.assertEqual("exited", spawner.container.status())
        self.assertEqual(0, len(self.job_manager.spawners))

    def test_kill_all_spawners(self):
        spawner_a = self.job_manager.start_new_spawner()
        spawner_b = self.job_manager.start_new_spawner()

        self.job_manager.kill_all_spawners()
        self.assertEqual("exited", spawner_a.container.status())
        self.assertEqual("exited", spawner_b.container.status())
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

        self.job_manager.kill_all_jobs()
        self.assertEqual(2, len(self.job_manager.jobs))
        status_dict = self.job_manager.list_jobs()
        self.assertFalse(status_dict[job_id_a]["running"])
        self.assertFalse(status_dict[job_id_b]["running"])

    def test_job_status(self):
        job_id = self.job_manager.start_job(self.host_list, self.interval)

        self.assertIsNone(self.job_manager.job_status("invalid_job_id"))

        status = self.job_manager.job_status()
        self.assertIsNotNone(status)
        self.assertTrue(status["running"])
        self.assertEqual(self.job_manager.jobs[job_id], status["delegates"])

        self.job_manager.kill_job(job_id)

        status = self.job_manager.job_status()
        self.assertIsNotNone(status)
        self.assertFalse(status["running"])
        self.assertEqual(self.job_manager.jobs[job_id], status["delegates"])

    def test_list_jobs(self):
        job_id_a = self.job_manager.start_job(self.host_list, self.interval)
        job_id_b = self.job_manager.start_job(self.host_list, self.interval)

        status_dict = self.job_manager.list_jobs()
        self.assertEqual(2, len(status_dict))
        self.assertTrue(status_dict[job_id_a]["running"])
        self.assertTrue(status_dict[job_id_b]["running"])
        self.assertEqual(self.job_manager.jobs[job_id_a], status_dict[job_id_a]["delegates"])
        self.assertEqual(self.job_manager.jobs[job_id_a], status_dict[job_id_b]["delegates"])

        self.job_manager.kill_all_jobs()

        status_dict = self.job_manager.list_jobs()
        self.assertEqual(2, len(status_dict))
        self.assertFalse(status_dict[job_id_a]["running"])
        self.assertFalse(status_dict[job_id_b]["running"])
        self.assertEqual(self.job_manager.jobs[job_id_a], status_dict[job_id_a]["delegates"])
        self.assertEqual(self.job_manager.jobs[job_id_a], status_dict[job_id_b]["delegates"])

    def tearDown(self):
        self.test_kill_all_spawners()