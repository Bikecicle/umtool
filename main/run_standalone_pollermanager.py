from model.PollerManager import PollerManager
from model.JobManager import JobManager
from model.Job import Host
from model.Job import Job
import sys

default_interval = 5

job_id = 1
if len(sys.argv) > 1:
    interval = float(sys.argv[1])
else:
    interval = default_interval
    print ("No interval given - set to default: " + str(default_interval) + "s")
host_list = []
host_list.append(Host("eb2tvx02drac.csc.ncsu.edu", "admin", "/*hoRV7or2C", "dell"))
host_list.append(Host("eb2-2214-sd01ipmi.csc.ncsu.edu", "admin", "sdteam18", "cisco"))
job = Job(job_id, interval, host_list)


poller_manager = PollerManager("placeholder")
print ("PollerManager created - " + str(poller_manager))
poller_manager.start_job(job)
