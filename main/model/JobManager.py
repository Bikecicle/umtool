import docker
from db.DatabaseMisc import DatabaseMisc
import db.DatabaseMisc as dm
from model.Job import Job

spawner_host_max = 1000
spawner_image = "spawner"

class JobManager:

    def __init__(self):
        self.client = docker.from_env()
        self.spawners = []
        self.jobs = {} # Maps job id to list of delegate spawner ids
        self.db = DatabaseMisc()

    # Resource Management

    def start_new_spawner(self):
        container = self.client.containers.run(spawner_image, detach=True, network_mode="host")
        print "beep"
        container.exec_run("python main/set_spawner_id.py " + container.id)
        spawner = Spawner(container)
        self.spawners.append(spawner)
        print ("New spawner running with ID: " + str(spawner.spawner_id))
        return spawner

    # Job Management

    def start_job(self, host_list, interval):
        # Assign job id
        job_id = dm.generate_unique_id()
        print ("New job with ID: " + str(job_id) + " - scanning " + str(len(host_list)) + " hosts every " + str(interval) + " seconds")

        # Delegate amongst spawners
        delegates = []
        for spawner in self.spawners:
            remaining_connections = spawner_host_max - spawner.total_hosts
            if remaining_connections > len(host_list):
                self.delegate(job_id, interval, host_list, spawner)
                host_list = []
                break
            else:
                host_subset = []
                for i in list(remaining_connections):
                    host_subset.append(host_list.remove())
                    self.delegate(job_id, interval, host_subset, spawner)
            delegates.append(spawner.spawner_id)

        # Create more spawners if host connections have maxed out
        while len(host_list) > 0:
            spawner = self.start_new_spawner()
            if len(host_list) < spawner_host_max:
                self.delegate(job_id, interval, host_list, spawner)
                host_list = []
            else:
                host_subset = []
                for i in list(spawner_host_max):
                    host_subset.append(host_list.remove())
                    self.delegate(job_id, interval, host_subset, spawner)
            delegates.append(spawner.spawner_id)

        # Map job id to delegate spawner ids
        self.jobs[id] = delegates

    def delegate(self, job_id, interval, host_list, spawner):
        spawner.jobs[job_id] = host_list
        spawner.total_hosts += len(host_list)
        self.db.create_job(Job(job_id, interval, host_list), spawner.spawner_id)

    def list_jobs(self):
        # TODO: See job_status
        pass

    def job_status(self, job_id):
        # TODO: Figure out format of job status to return
        pass

    def kill_job(self, job_id):
        self.db.kill_job(job_id)

    def kill_all_jobs(self):
        for job_id in self.jobs:
            self.kill_job(job_id)

class Spawner:

    def __init__(self, container):
        
        self.container = container
        self.spawner_id = container.id
        self.jobs = {} # Maps job id to list of hosts
        self.total_hosts = 0

def main():
    job_manager = JobManager()
    #TODO: Implement default behavior of job manager

if __name__ == '__main__':
    main()
