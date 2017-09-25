
class ServerUsageReport:
    def __init__(self, unique_id, unix_epoch_timestamp, cpu_temp):
        self.unique_id = unique_id
        self.unix_epoch_timestamp = unix_epoch_timestamp
        self.cpu_temp = cpu_temp

    # Return a plain-text representation of a usage report row
    def get_string_row(self):
        return "exampleID, 1506360452, 30"

