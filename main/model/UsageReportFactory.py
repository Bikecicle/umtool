from main.model.ServerUsageReport import ServerUsageReport
from time import time
#from PackagedSensorReading import PackagedSensorReading
#from pyghmi.ipmi import command


class UsageReportFactory:
    def __init__(self, ipmi, unique_id):
        self.ipmi = ipmi
        self.unique_id = unique_id

    def get_usage_report(self):
        readings = list(self.ipmi.get_sensor_data())
        timestamp = int(round(time() * 1000))
        return ServerUsageReport(self.unique_id, timestamp, readings)
