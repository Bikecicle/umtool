from db.DatabaseMisc import DatabaseMisc
from model.Poller import Poller
import thread


class PollerManager:
    def __init__(self, spawner_id):
        self.pollers = {}  # Dictionary mapping job id to Poller object
        self.spawner_id = spawner_id
        self.db = DatabaseMisc()

    def check_database_state(self):
        # Check for new jobs
        jobs = self.db.check_job_assignments(self.spawner_id)
        for job in jobs:
            if not self.pollers.has_key(job.job_id):
                # Create new poller, start polling, and store in map
                poller = Poller(job.host_list, job.interval)
                poller.start()
                self.pollers[job.job_id] = poller

        # Check for kill commands
        for job_id in self.pollers:
            if self.db.check_kill_order(job_id):
                self.pollers[job_id].kill()
                self.db.spawner_report_death_complete(job_id, self.spawner_id)