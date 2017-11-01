import DatabaseMisc


class ServerConnection:
    # @param Hostname: Just a string with the server to connect to
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
    def __init__(self, usage_report_factory, save_method="d", text_file_path=""):
        self.usage_report_factory = usage_report_factory
        self.save_method = save_method
        self.usage_report_data = []  # Only used if save_method 'm' flag is set
        self.text_file_path = text_file_path  # Only used if save_method 't' flag is set
        self.db_connection = DatabaseMisc()

    # Polls the hostname and then saves the usage report to the database
    def poll_connection_and_save_usage_report(self):
        usage_report = self.usage_report_factory.get_usage_report()

        # Set flags
        if 'd' in self.save_method:
            # save to database
            self.db_connection.save_usage_report(usage_report)
        if 'm' in self.save_method:
            pass
        if 't' in self.save_method:
            pass
        if 'p' in self.save_method:
            pass
