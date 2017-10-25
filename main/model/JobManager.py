import docker

spawner_host_max = 1000
spawner_image = "" # TODO: decide on spawner container image name

class JobManager:

    def __init__(self):
        self.client = docker.from_env()
        self.spawners = []
        self.jobs = {} # Maps job id to list of delegate spawners

    # Resource Management

    def start_new_spawner(self):
        spawner = Spawner(self.client.containers.run(spawner_image, detach=True))
        self.spawners.append(spawner)
        return spawner

    # Job Management

    def start_job(self, hosts, frequency, duration):
        # Assign job id
        # TODO
        id = 0

        # Delegate amongst spawners
        delegates = []
        for spawner in self.spawners:
            remaining_connections = spawner_host_max - spawner.total_hosts
            if remaining_connections > len(hosts):
                spawner.add_job(id, hosts, frequency, duration)
                hosts = []
                break
            else:
                host_subset = []
                for i in list(remaining_connections):
                    host_subset.append(hosts.remove())
                spawner.add_job(id, host_subset, frequency, duration)
            delegates.append(spawner)

        # Create more spawners if host connections have maxed out
        while len(hosts) > 0:
            spawner = self.start_new_spawner()
            if len(hosts) < spawner_host_max:
                spawner.add_job(id, hosts, frequency, duration)
                hosts = []
            else:
                host_subset = []
                for i in list(spawner_host_max):
                    host_subset.append(hosts.remove())
                spawner.add_job(id, host_subset, frequency, duration)
            delegates.append(spawner)

        # Map job id to delegate spawners
        self.jobs[id] = delegates

    def list_jobs(self):
        for id in self.jobs:
            self.job_status(id)
        # TODO: see job_status()

    def job_status(self, id):
        for spawner in self.jobs[id]:
            spawner.job_status(id)
        # TODO: figure out how to present status and combine reports from delegates

    def kill_job(self, id):
        for spawner in self.jobs[id]:
            spawner.kill_job(id)

    def kill_all_jobs(self):
        for spawner in self.spawners:
            spawner.kill_all_jobs()

class Spawner:

    def __init__(self, container):
        
        self.id = id
        jobs = {} # Maps job id to list of hosts
        total_hosts = 0

    # The following functions will be implemented based on how commands will be sent to the manager running on the container

    # TODO: def add_job(self, id, hosts, frequency, duration):

    # TODO: def job_status(self, id):

    # TODO: def kill_job(self, id):

    # TODO: def kill_all_jobs(self):