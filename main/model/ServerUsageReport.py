class ServerUsageReport:
    def __init__(self, unique_id, unix_epoch_timestamp, sensor_readings):
        self.unique_id = unique_id
        self.unix_epoch_timestamp = unix_epoch_timestamp
        self.sensor_reading = sensor_readings
