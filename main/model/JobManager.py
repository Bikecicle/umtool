import docker
from main.db.DatabaseMisc import DatabaseMisc
from main.db.DatabaseMisc import generate_unique_id
from main.model.Job import Job

DEFAULT_SPAWNER_HOST_MAX = 1000
SPAWNER_IMAGE = "spawner"


class JobManager:

    def __init__(self, spawner_host_max=None):
        self.client = docker.from_env()
        self.spawners = []
        self.jobs = {} # Maps job id to list of delegate spawner ids
        self.db = DatabaseMisc()

        if not spawner_host_max:
            spawner_host_max = DEFAULT_SPAWNER_HOST_MAX
        
        self.spawner_host_max = spawner_host_max

    # Resource Management

    def start_new_spawner(self):
        container = self.client.containers.run(SPAWNER_IMAGE, detach=True, network_mode="host")
        container.exec_run("python main/set_spawner_id.py " + container.id)
        spawner = Spawner(container)
        self.spawners.append(spawner)
        print ("New spawner running with ID: " + str(spawner.spawner_id))
        return spawner

    # Job Management

    def start_job(self, host_list, interval):
        # Assign job id
        job_id = generate_unique_id()
        print ("New job with ID: " + str(job_id) + " - scanning " + str(len(host_list)) + " hosts every " + str(interval) + " seconds")

        # Delegate amongst spawners
        delegates = []
        for spawner in self.spawners:
            remaining_connections = self.spawner_host_max - spawner.total_hosts
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
            if len(host_list) < self.spawner_host_max:
                self.delegate(job_id, interval, host_list, spawner)
                host_list = []
            else:
                host_subset = []
                for i in list(self.spawner_host_max):
                    host_subset.append(host_list.remove())
                    self.delegate(job_id, interval, host_subset, spawner)
            delegates.append(spawner.spawner_id)

        # Map job id to delegate spawner ids
        self.jobs[job_id] = delegates
        return job_id

    def delegate(self, job_id, interval, host_list, spawner):
        spawner.jobs[job_id] = host_list
        spawner.total_hosts += len(host_list)
        self.db.create_job(Job(job_id, interval, host_list), spawner.spawner_id)

    def list_jobs(self):
        status_dict = {}
        for job_id in self.jobs:
            status_dict[job_id] = self.job_status(job_id)
        return status_dict

    def job_status(self, job_id):
        if job_id in self.jobs:
            return {"running": not self.db.check_if_job_is_fully_dead(job_id), "delegates": self.jobs[job_id]}
        else:
            return None

    def kill_job(self, job_id):
        if job_id in self.jobs:
            self.db.kill_job(job_id)
            self.jobs.pop(job_id)
            return True
        else:
            return False

    def kill_all_jobs(self):
        for job_id in self.jobs:
            self.db.kill_job(job_id)
        self.jobs = {}

    def kill_spawner(self, spawner_id):
        success = False
        for spawner in self.spawners:
            if spawner.spawner_id == spawner_id:
                spawner.container.kill()
                spawner.container.remove()
                self.spawners.remove(spawner)
                success = True
                break
        return success

    def kill_all_spawners(self):
        for spawner in self.spawners:
            spawner.container.kill()
            spawner.container.remove()
        self.spawners = []

class Spawner:

    def __init__(self, container):
        
        self.container = container
        self.spawner_id = container.id
        self.jobs = {} # Maps job id to list of hosts
        self.total_hosts = 0
