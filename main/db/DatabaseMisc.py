from __future__ import print_function

import random

from pymongo import MongoClient
import MongoObjectSerialization as mos

# How many bits to use for unique IDs
NUM_ID_BITS = 4096


class DatabaseMisc:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.utilize
        self.job_table = self.db.job_tracking_table
        self.usage_report_table = self.db.usage_report_table

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

    # Start a job given a jobID, spawner ID, list of hosts (objects)
    #
    # Returns true if the creation was successful. Otherwise false, but it will probably throw an exception
    # Any exceptions this method throws should be caught, so report them to whoever is in charge of maintaining
    # this method
    # TODO: Maybe use model.Job.Job here too? - Griffin
    def create_job(self, job_object, spawner_id):
        """
        :param job_object:
        :type job_object: Job.Job
        :param spawner_id:
        :type spawner_id: str
        :return:
        """
        # TODO: See if job already exists

        # Get the core of the job
        doc = mos.get_job_serialization(job_object)

        # This is what's not going to be in the job (unless that model gets changed around)
        doc['active'] = True
        doc['spawner_id'] = spawner_id

        doc = {
            'job_id': str(job_object.job_id),
            'spawner_id': str(spawner_id),
            'active': True,
            'interval': int(job_object.interval),
            'hosts': job_object.host_list
        }

        # TODO: Remove, testing purposes only

        # Insert into db
        result = self.job_table.insert_one(doc)

        return result

    # Save usage report to the database
    def save_usage_report(self, usage_report):
        doc = usage_report.get_document_serialization()
        result = self.usage_report_table.insert_one(doc)
        return result

    # Generate a random string that serves as a unique ID for any purpose
    @staticmethod
    def generate_unique_id():
        return str(hex(random.getrandbits(NUM_ID_BITS)))
