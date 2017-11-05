from model.JobManager import JobManager
from model.Job import Host
from model.Job import Job
import sys

job_id = 1
interval = sys.argv[1]
host_list = []
#host_list.append(Host("eb2tvx02drac.csc.ncsu.edu", "admin", "/*hoRV7or2C", "dell"))
host_list.append(Host("eb2-2214-sd01ipmi.csc.ncsu.edu", "admin", "sdteam18", "cisco"))
job = Job(job_id, interval, host_list)


poller_manager = PollerManager()
print "PollerManager created - " + str(poller_manager) + "/n"
poller_manager.start_job(job)
