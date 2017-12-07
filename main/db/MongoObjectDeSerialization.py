from main.model.Job import Job, Host


# This class is dedicated to converting MongoDB docs and iterators to specified objects
def get_document_serialization(sensor_reading):
    doc = {
        "type": sensor_reading.type,
        "value": sensor_reading.value,
        "units": sensor_reading.units,
        "name": sensor_reading.name
    }

    return doc


def get_job_list_deserialization(job_iterator):
    jobs_list = [get_job_deserialization(job_doc) for job_doc in job_iterator]

    return jobs_list


def get_host_list_deserialization(host_iterator):
    host_list = [get_host_deserialization(host_doc) for host_doc in host_iterator]

    return host_list


def get_host_deserialization(host_document):
    hostname = host_document['hostname']
    userid = host_document['username']
    password = host_document['password']
    unique_id = host_document['unique_id']
    host = Host(
        hostname=hostname,
        userid=userid,
        password=password,
        unique_id=unique_id
    )

    return host


def get_job_deserialization(job_document):
    # job Job = Job()
    job_id = job_document['job_id']
    interval = job_document['interval']
    host_list = get_host_list_deserialization(job_document['host_list'])
    active = job_document['active']

    job = Job(
        job_id=job_id,
        interval=interval,
        host_list=host_list,
        active=active
    )

    return job
