from db.DatabaseMisc import DatabaseMisc
from model.ServerUsageReport import ServerUsageReport
import threading
import time


class ServerConnection (threading.Thread):
    def __init__(self, ipmi, unique_id):
        threading.Thread.__init__(self)
        self.ipmi = ipmi
        self.unique_id = unique_id

        self.db_connection = DatabaseMisc()

    def run(self):
        self.poll_connection_and_save_usage_report()

    # Polls the hostname and then saves the usage report to the database
    def poll_connection_and_save_usage_report(self):
        readings = list(self.ipmi.get_sensor_data())
        timestamp = int(round(time.time() * 1000))
        usage_report = ServerUsageReport(self.unique_id, timestamp, readings)
        self.db_connection.save_usage_report(usage_report)
