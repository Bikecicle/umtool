from pyghmi.ipmi import command
from UsageReportFactory import UsageReportFactory
from ServerConnection import ServerConnection
import time


class Poller:
    # @param host_list: Just a list of strings with the server to connect to
    #       This could be something like "10.2.2.2" or "abc.ncsu.edu"
    #
    # @param usage_report_factory: Must implement the get_usage_report(hostname) method
    #
    #  @param save_method
    #       This is a set of flags that determines how the usage reports should be saved
    #       Flags:
    #       d = database
    #       m = memory (store in list)
    #       t = text file (requires text file path be set)
    #       p = print to standard output
    #  Examples:
    #       save_method = "dm" -- save to the database and memory
    #       save_method = "tmd" -- save to a text file and memory and the database
    #
    # @param text_file_path
    #       If using the "t" flag for save_method, this option must be set
    #       so that the save flag
    #
    def __init__(self, host_list, interval, save_method='', text_file_prefix=''):
        self.interval = interval  # Polling interval in seconds
        self.server_connection_list = []
        self.save_method = save_method
        self.text_file_prefix = text_file_prefix
        self.stopped = False
        for host in host_list:
            text_file_path = self.text_file_prefix  # Later on, this will be based on the host

            ipmi = command.Command(bmc=host.hostname, userid=host.userid, password=host.password)
            usage_report_factory = UsageReportFactory(ipmi, host.unique_id)
            server_connection = ServerConnection(usage_report_factory,
                                                 self.save_method,
                                                 text_file_path)
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
