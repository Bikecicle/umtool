from __future__ import print_function

import random

from pymongo import MongoClient

# How many bits to use for unique IDs
NUM_ID_BITS = 4096


# Sets the "active" flag of a job to false
def kill_job(job_id):
    pass


# Check if all poller managers are inactive for a particular job
def check_if_job_is_fully_dead(job_id):
    pass


# Check if a job is supposed to die
def check_job_orders(job_id):
    pass


# Start a job given a jobID, container ID and a list of dictionaries with the below spec:
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
def createJob(jobID, containerID, hostInfo):
    # Create job
    pass

    return True


# Save usage report to the database
def save_usage_report(usage_report):
    doc = usage_report.get_document_serialization()
    db = MongoClient().test
    result = db.server_usage_reports.insert_one(doc)
    print(result)


# Generate a random string that serves as a unique ID for any purpose
def generate_unique_id():
    return str(hex(random.getrandbits(NUM_ID_BITS)))
