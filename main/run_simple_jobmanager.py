from model.JobManager import JobManager
from model.Job import Host
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


job_manager = JobManager()
print ("JobManager created - " + str(job_manager))
job_manager.start_job(host_list, interval)
output = job_manager.spawners[0].container.attach(stream=True)
