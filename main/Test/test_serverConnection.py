from unittest import TestCase
from model.ServerConnection import ServerConnection
import time


class TestServerConnection(TestCase):
    def test_poll_connection_and_save_usage_report(self):
        ipmi = MockIPMI()
        database = MockDB()
        server_connection = ServerConnection(ipmi, "unique")

        server_connection.db_connection = database

        ts = time.time() * 1000
        server_connection.run()
        time.sleep(1)

        self.assertEqual(ipmi.data, database.saved_usage_report.sensor_reading)
        self.assertAlmostEqual(ts, database.saved_usage_report.unix_epoch_timestamp, delta=100)
        self.assertEqual(server_connection.unique_id, database.saved_usage_report.unique_id)


class MockIPMI:
    def __init__(self):
        self.data = [{"name": "sensor1", "value": 1}, {"name": "sensor2", "value": 2}]

    def get_sensor_data(self):
        return self.data

class MockDB:

    def __init__(self):
        self.saved_usage_report = None

    def save_usage_report(self, usage_report):
        self.saved_usage_report = usage_report
