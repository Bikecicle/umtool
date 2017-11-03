from pyghmi.ipmi import command
from UsageReportFactory import UsageReportFactory
from ServerConnection import ServerConnection
import time


class Poller:
    def __init__(self, host_list, interval):
        self.interval = interval  # Polling interval in seconds
        self.server_connection_list = []
        self.stopped = False
        for host in host_list:
            text_file_path = self.text_file_prefix  # Later on, this will be based on the host

            ipmi = command.Command(bmc=host.hostname, userid=host.userid, password=host.password)
            usage_report_factory = UsageReportFactory(ipmi, host.unique_id)
            server_connection = ServerConnection(usage_report_factory)
            self.server_connection_list.append(server_connection)

    def poll_servers(self):
        while not self.stopped:
            t_start = time.time()
            for server_connection in self.server_connection_list:
                server_connection.poll_connection_and_save_usage_report()
                if self.stopped:
                    break
            t_end = time.time()
            t_delta = t_end - t_start
            # Wait until end of polling interval (unless polling took longer than interval)
            if t_delta < self.interval:
                time.sleep(self.interval - t_delta)

    def kill(self):
        self.stopped = True
