

class PollerManager:

    def __init__(self):
        self.pollers = {} # Dictionary mapping job id to Poller object
        self.container_id
        self.db

    def check_database_state(self):
        # Check for new jobs
        jobs = self.db.list_current_jobs(self.spawner_id)
        # TODO: parse received job info for new jobs and then start new pollers to execute them

        # Check for kill commands

        # Update database

    # TODO: def start_job(self, id, hosts, frequency)

    # TODO: def kill_job(self, id)