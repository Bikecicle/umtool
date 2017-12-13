class Job:
    def __init__(self, job_id, interval, host_list, active=True):
        self.job_id = job_id
        self.interval = interval
        self.host_list = host_list
        self.active = active


class Host:
    def __init__(self, hostname, userid, password, unique_id):
        self.hostname = hostname
        self.userid = userid
        self.password = password
        self.unique_id = unique_id
