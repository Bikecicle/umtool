class ServerUsageReport:
    def __init__(self, unique_id, unix_epoch_timestamp, packaged_sensor_readings):
        self.unique_id = unique_id
        self.unix_epoch_timestamp = unix_epoch_timestamp
        self.packaged_sensor_readings = packaged_sensor_readings

    def get_document_serialization(self):
        serialized_readings = [packaged_sensor_reading.get_document_serialization()
                               for packaged_sensor_reading in self.packaged_sensor_readings]

        doc = {
            "unique_id": str(self.unique_id),
            "timestamp": long(self.unix_epoch_timestamp),
            "readings": serialized_readings
        }

        return doc

