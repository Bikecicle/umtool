from unittest import TestCase
from main.model import JobManager
import docker


class TestJobManager(TestCase):
    def setUp(self):
        self.job_manager = JobManager()
        self.client = docker.from_env()

    def test_start_new_spawner_and_delegate(self):
        # Check if creation was successful
        spawner = self.job_manager.start_new_spawner()
        self.assertIsNotNone(spawner)
        self.assertEqual("running", spawner.container.status())
        self.assertEqual(1, len(self.job_manager.spawners))

        # Check if spawner is running python script internally
        if "python" not in spawner.container.top():
            self.fail("Spawner not running script")

        # TODO: test delegate() on existing spawner

        # Kill spawner
        self.job_manager.kill_spawner()
        self.assertEqual("exited", spawner.container.status())
        self.assertEqual(0, len(self.job_manager.spawners))



    def test_start_and_kill_job(self):
        # Check if job creation was successful
        host_list = []
        interval = 1
        job_id = self.job_manager.start_job(host_list, interval)
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
        self.fail()

    def tearDown(self):
        pass