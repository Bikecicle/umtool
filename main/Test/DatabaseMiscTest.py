from __builtin__ import range
import unittest2 as unittest
from Utils import Config
import random

from model.Job import Job
from db import DatabaseMisc as dm
from model.Job import Host

# How many bits to use for generating random test data
NUM_TEST_BITS = 10


def generate_mock_host_list(num_hosts):
    host_list = []
    for _ in range(num_hosts):
        host = Host(str(random.getrandbits(NUM_TEST_BITS)),
                    str(random.getrandbits(NUM_TEST_BITS)),
                    str(random.getrandbits(NUM_TEST_BITS)),
                    str(random.getrandbits(NUM_TEST_BITS)))

        host_list.append(host)
    return host_list


class TestDatabaseMisc(unittest.TestCase):
    def setUp(self):
        self.job_id = dm.generate_unique_id()
        self.spawner_a_id = dm.generate_unique_id()
        self.spawner_b_id = dm.generate_unique_id()
        self.host_list = generate_mock_host_list(2000)

        self.host_list_a = self.host_list[0:1000]
        self.host_list_b = self.host_list[1000:2000]

        self.db_obj = dm.DatabaseMisc()

        # Sanity check to make sure I still know how to index lists/arrays
        assert (len(self.host_list_a) == len(self.host_list_b) == 1000)

    def test_create_job(self):
        # Create a job for each container
        # Note that at this point we've already got a job id and container IDs, and we're just supplying them
        # to the method

        job_a = Job(self.job_id, 30, self.host_list_a)

        # Create the job
        result = self.db_obj.create_job(job_a, self.spawner_a_id)

        self.assertTrue(result)  # Make sure creation was successful

        self.db_obj.check_job_assignments(self.spawner_a_id)


    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
