

def get_document_serialization(sensor_reading):
    doc = {
        "type": sensor_reading.type,
        "value": sensor_reading.value,
        "units": sensor_reading.units,
        "name": sensor_reading.name
    }

    return doc
