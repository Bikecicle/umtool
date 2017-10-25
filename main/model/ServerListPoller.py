from pyghmi.ipmi import command
from UsageReportFactory import UsageReportFactory
from ServerConnection import ServerConnection

class ServerListPoller:
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
    def __init__(self, host_list, save_method='', text_file_prefix=''):
        self.host_list = host_list
        # TODO: Will we ever modify the connection list at runtime?
        self.server_connection_list = []
        self.save_method = save_method
        self.text_file_prefix = text_file_prefix

        self._init_server_connection_list()

    def poll_servers(self):
        for server_connection in self.server_connection_list:
            server_connection.poll_connection_and_save_usage_report()

    def _init_server_connection_list(self):
        for host in self.host_list:
            text_file_path = self.text_file_prefix  # Later on, this will be based on the host
            ipmi = command.Command(bmc=host.hostname, userid=host.userid, password=host.password)
            usage_report_factory = UsageReportFactory(ipmi, host)
            server_connection = ServerConnection(usage_report_factory,
                                                 self.save_method,
                                                 text_file_path)
            self.server_connection_list.append(server_connection)
