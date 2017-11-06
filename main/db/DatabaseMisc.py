from __future__ import print_function

import random

from pymongo import MongoClient
import MongoObjectSerialization as mos
import MongoObjectDeSerialization as mods

# How many bits to use for unique IDs
NUM_ID_BITS = 4096


# Generate a random string that serves as a unique ID for any purpose
def generate_unique_id():
    return str(hex(random.getrandbits(NUM_ID_BITS)))


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
        query = {
            'spawner.spawner_id': spawner_id
        }
        result = self.job_table.find(query)

        jobs_list = mods.get_job_list_deserialization(result)

        return jobs_list

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
        doc['spawner'] = {
            'spawner_id': spawner_id,
            'active': True
        }

        # Insert into db
        result = self.job_table.insert_one(doc)

        return result

    # Save usage report to the database
    def save_usage_report(self, usage_report):
        doc = mos.get_server_usage_report_serialization(usage_report)
        result = self.usage_report_table.insert_one(doc)
        return result

