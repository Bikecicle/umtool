from ServerUsageReport import ServerUsageReport
from PackagedSensorReading import PackagedSensorReading
from pyghmi.ipmi import command


class UsageReportFactory:
    def __init__(self, ipmi, unique_id):
        self.ipmi = ipmi
        self.unique_id = unique_id


    def get_usage_report(self):
        readings = list(self.ipmi.get_sensor_data())
        trimmed_readings = []
        for r in readings:
            trimmed_readings.append(PackagedSensorReading(r))
        timestamp = 0 # Get real timestamp here
        return ServerUsageReport(self.unique_id, timestamp, trimmed_readings)