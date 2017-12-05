from bottle import route, run, post, request
from model.JobManager import JobManager
from model.Job import Job, Host
from db import DatabaseMisc as dm

job_manager = None


def main():
    global job_manager

    job_manager = JobManager()

    run(host='localhost', port=8080, debug=True)

# Test functions


@route('/hello')
def hello():
    return "Hello World!"


@post('/create_simple_job')
def create_simple_job():
    host_list = [Host("eb2-2214-sd01ipmi.csc.ncsu.edu", "admin", "sdteam18", "cisco")]
    job_id = dm.generate_unique_id()
    interval = 3

    job_manager.start_job(host_list, interval)
    
# Project API


@post('/start_job')  # TODO: figure out how to pass in csv then convert to list of host objects
def start_job():
    content = request.json
    interval = content['interval']
    host_list_json = content['hosts']
    host_list = []
    for host_json in host_list_json:
        host = Host(host_json['hostname'], host_json['username'], host_json['password'], host_json['unique_id'])
        host_list.append(host)
    job_manager.start_job(host_list, interval)


@route('/list_jobs', method='GET')
def list_jobs():
    status_list = job_manager.list_jobs()
    return {"success": True, "status": str(status_list)}

    
@route('/job_status/<job_id>', method='GET')
def job_status(job_id):
    status = job_manager.job_status(job_id)
    if status:
        return {"success": True, "status": str(status)}
    else:
        return {"success": False}


@route('/kill_job/<job_id>', method='POST')
def kill_job(job_id):
    if job_manager.kill_job(job_id):
        return {"success": True}
    else:
        return {"success": False}


@route('/kill_all_jobs', method='POST')
def kill_all_jobs():
    job_manager.kill_all_jobs()
    return {"success": True}


@route('/kill_spawner/<spawner_id>', method='POST')
def kill_spawner(spawner_id):
    if job_manager.kill_spawner(spawner_id):
        return {"success": True}
    else:
        return {"success": False}


@route('/kill_all_spawners', method='POST')
def kill_all_spawners():
    job_manager.kill_all_spawners
    return {"success": True}


if __name__ == '__main__':
    main()
