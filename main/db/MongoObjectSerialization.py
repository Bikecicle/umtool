# This class is dedicated to converting objects to MongoDB compatible objects
def get_document_serialization(sensor_reading):
    doc = {
        "type": sensor_reading.type,
        "value": sensor_reading.value,
        "units": sensor_reading.units,
        "name": sensor_reading.name
    }

    return doc


def get_job_serialization(job_object):
    """

    :param job_object:
    :type job_object: Job.Job
    :return:
    """

    doc = {
        'job_id': job_object.job_id,
        'interval': job_object.interval,
        'host_list': [get_host_serialization(host) for host in job_object.host_list]
    }

    return doc


def get_host_serialization(host_object):
    """

    :param host_object:
    :type host_object: Job.Host
    :return:
    """

    doc = {
        'hostname': host_object.hostname,
        'username': host_object.userid,
        'password': host_object.password,
        'unique_id': host_object.unique_id
    }

    return doc
