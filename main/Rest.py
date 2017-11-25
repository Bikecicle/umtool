from bottle import route, run, post
from model.JobManager import JobManager
from model.Job import Job, Host
from db import DatabaseMisc as dm
import sys

job_manager = None


def main():
    global job_manager

    job_manager = JobManager()

    run(host='localhost', port=8080, debug=True)


@route('/hello')
def hello():
    return "Hello World!"


@post('/create_simple_job')
def create_simple_job():
    host_list = [Host("eb2-2214-sd01ipmi.csc.ncsu.edu", "admin", "sdteam18", "cisco")]
    job_id = dm.generate_unique_id()
    interval = 30
    job = Job(job_id, interval, host_list)

    job_manager.start_job(job)

if __name__ == '__main__':
    main()
