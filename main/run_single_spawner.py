from model import JobManager
from Job import Host
import sys

def main():

    interval = sys.argv[1]
    host_list = []
    host_list.append(Host("eb2tvx02drac.csc.ncsu.edu", "admin", "/*hoRV7or2C", "dell"))
    host_list.append(Host("eb2-2214-sd01ipmi.csc.ncsu.edu", "admin", "sdteam18", "cisco"))

    job_manager = JobManager()
    job_manager.start_new_spawner()

    job_manager.start_job(host_list, interval)