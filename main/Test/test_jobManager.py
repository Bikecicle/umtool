from unittest import TestCase
from main.model import JobManager
import docker


class TestJobManager(TestCase):
    def setUp(self):
        self.job_manager = JobManager()
        self.client = docker.from_env()

        self.host_list_a
        self.host_list_b
        self.interval

    def test_start_new_spawner_and_delegate(self):
        # Check if creation was successful
        spawner = self.job_manager.start_new_spawner()
        self.assertIsNotNone(spawner)
        self.assertEqual("running", spawner.container.status())
        self.assertEqual(1, len(self.job_manager.spawners))

        # Check if spawner is running python script internally
        if "python" not in spawner.container.top():
            self.fail("Spawner not running script")

        # Kill spawner
        self.job_manager.kill_spawner()
        self.assertEqual("exited", spawner.container.status())
        self.assertEqual(0, len(self.job_manager.spawners))



    def test_start_and_kill_job(self):
        # Check if job creation was successful
        job_id = self.job_manager.start_job(self.host_list_a, self.interval)
        self.assertIsNotNone(job_id)
        self.assertEqual(1, len(self.job_manager.jobs))
        status = self.job_manager.job_status(job_id)
        self.assertIsNotNone(status)
        self.assertTrue(status["running"])

        # Kill job
        self.job_manager.kill_job(job_id)
        self.assertEqual(0, len(self.job_manager.jobs))
        status = self.job_manager.job_status(job_id)
        self.assertFalse(status["running"])

    def test_multi_start_and_kill_job(self):
        # Check if job creation was successful
        job_id_a = self.job_manager.start_job(self.host_list_a, self.interval)
        job_id_b = self.job_manager.start_job(self.host_list_b, self.interval)
        self.assertIsNotNone(job_id_a)
        self.assertIsNotNone(job_id_b)
        self.assertEqual(2, len(self.job_manager.jobs))
        status_list = self.job_manager.list_jobs()
        self.assertTrue(status_list[0]["running"])
        self.assertTrue(status_list[1]["running"])

        # Kill jobs
        self.job_manager.kill_all_jobs()
        self.assertEqual(0, len(self.job_manager.jobs))
        status_list = self.job_manager.list_jobs()
        self.assertFalse(status_list[0]["running"])
        self.assertFalse(status_list[1]["running"])

    def tearDown(self):
        pass