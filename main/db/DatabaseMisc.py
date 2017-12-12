from __future__ import print_function

import random

from pymongo import MongoClient
import db.MongoObjectSerialization as mos
import db.MongoObjectDeSerialization as mods

# How many bits to use for unique IDs
NUM_ID_BITS = 2048


# Generate a random string that serves as a unique ID for any purpose
def generate_unique_id():
    return str(hex(random.getrandbits(NUM_ID_BITS)))


class DatabaseMisc:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.utilize
        self.job_table = self.db.job_tracking_table
        self.usage_report_table = self.db.usage_report_table
    
    # Drop whatever tables need to be dropped
    # By default, drops the job table but not the usage
    # table
    def drop_tables(usage_table=False, job_table=True):
        if usage_table: self.usage_report_table.drop()
        if job_table: self.job_table.drop()

    # Sets the "active" flag of a job to false for all of its entries
    # Returns true if successful, false otherwise (as of now, this will never happen--exceptions need to be caught as
    # they appear and handled by returning false)
    def kill_job(self, job_id):
        query = {
            'job_id': job_id
        }

        results = self.job_table.find(query)

        for result in results:
            result['active'] = False
            self.job_table.save(result)

        return True

    # Check if all poller managers are inactive for a particular job
    # Returns true if job is fully dead, false otherwise
    def check_if_job_is_fully_dead(self, job_id):
        query = {
            'job_id': job_id
        }

        result_iterator = self.job_table.find(query)

        job_is_fully_dead = True

        for result in result_iterator:
            # Each "result" will be a job entry in the database, which may or may not be active
            spawner_is_active = result['active']
            if spawner_is_active:
                job_is_fully_dead = False
                break

        return job_is_fully_dead

    # Call this method (as a spawner) to report that you have successfully terminated your part of a job
    def spawner_report_death_complete(self, job_id, spawner_id):
        query = {
            'job_id': job_id,
            'spawner.spawner_id': spawner_id
        }

        result = self.job_table.find_one(query)

        result['spawner']['active'] = False

        self.job_table.save(result)

    # Check if a job is supposed to die
    # Return true if yes, false if no
    def check_kill_order(self, job_id):
        query = {
            'job_id': job_id
        }

        result = self.job_table.find_one(query)

        job_active = result['active']

        return not job_active

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
