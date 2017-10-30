from builtins import range
import random
import unittest
from Utils import Config
from db import DatabaseMisc as dm

# How many bits to use for generating random test data
NUM_TEST_BITS = 10


def generate_mock_host_list(num_hosts):
    host_list = []
    for i in range(num_hosts):
        host = {'hostname': str(random.getrandbits(NUM_TEST_BITS)),
                'username': str(random.getrandbits(NUM_TEST_BITS)),
                'password': str(random.getrandbits(NUM_TEST_BITS))}
        host_list.append(host)
    return host


class TestDatabaseMisc(unittest.TestCase):
    def setUp(self):
        self.job_id = dm.generate_unique_id()
        self.container_a_id = dm.generate_unique_id()
        self.container_b_id = dm.generate_unique_id()
        self.host_list = dm.generate_mock_host_list(2000)

        self.host_list_a = self.host_list[0:1000]
        self.host_list_b = self.host_list[1000:2000]

        # Sanity check to make sure I still know how to index lists/arrays
        assert(len(self.host_list_a) == len(self.host_list_b) == 2000)

    def test_create_job(self):
        # Create a job for each container
        # Note that at this point we've already got a job id and container IDs, and we're just supplying them
        # to the method

        # Create the job
        result = dm.createJob(self.job_id, self.container_a_id, self.host_list_a)

        self.assertTrue(result)  # Make sure creation was successful
        # At this point

    def tearDown(self):
        pass
