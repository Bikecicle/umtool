from __future__ import print_function

import random

from pymongo import MongoClient

# How many bits to use for unique IDs
NUM_ID_BITS = 4096


class DatabaseMisc:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.utilize

    # Sets the "active" flag of a job to false
    def kill_job(self, job_id):
        pass

    # Check if all poller managers are inactive for a particular job
    def check_if_job_is_fully_dead(self, job_id):
        pass

    # Check if a job is supposed to die
    def check_kill_order(self, job_id):
        pass

    # Check assigned jobs for a given spawner (returns list of Job data structures - see model.Job.Job)
    def check_job_assignments(self, spawner_id):
        pass

    # Start a job given a jobID, spawner ID and a list of dictionaries with the below spec:
    #
    # (hostnameDictionaryList)
    # {"hostname": <host_string>,
    # "username": <username_string>,
    # "password": <password_string
    # }
    #
    # Returns true if the creation was successful. Otherwise false, but it will probably throw an exception
    # Any exceptions this method throws should be caught, so report them to whoever is in charge of maintaining
    # this method
    # TODO: Maybe use model.Job.Job here too? - Griffin
    def create_job(self, job_id, spawner_id, host_info):
        # TODO: See if job already exists

        # Create new job with spawner ID
        doc = {
            'job_id': job_id,
            'spawner_id': spawner_id,
            'active': True,
            'hosts': host_info
        }

        # Insert into db
        return True

    # Save usage report to the database
    def save_usage_report(self, usage_report):
        doc = usage_report.get_document_serialization()
        result = self.db.server_usage_reports.insert_one(doc)

    # Generate a random string that serves as a unique ID for any purpose
    @staticmethod
    def generate_unique_id():
        return str(hex(random.getrandbits(NUM_ID_BITS)))