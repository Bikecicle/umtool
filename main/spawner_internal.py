from model.PollerManager import PollerManager
import time


loop_interval = 5

def main():
    # Wait to be assigned a spawner id
    spawner_id = ""
    while spawner_id == "":
        f = open("main/spawner_id", "r")
        spawner_id = f.read()
    print ("Assigned spawner id: " + spawner_id)

    # Execute loop
    poller_manager = PollerManager(spawner_id)
    while True:
        poller_manager.check_database_state()
        time.sleep(loop_interval)

if __name__ == '__main__':
    main()


