

class PackagedSensorReading:
    def __init__(self, sensor_reading):
        self.type = sensor_reading.type
        self.value = sensor_reading.value
        self.units = sensor_reading.units
        self.name = sensor_reading.name
        # Everything else is thrown out

    def get_document_serialization(self):
        doc = {
            "type": self.type,
            "value": self.value,
            "units": self.units,
            "name": self.name
        }

        return doc
