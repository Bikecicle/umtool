from __future__ import print_function
from pymongo import MongoClient


def save_usage_report(usage_report):
    doc = usage_report.get_document_serialization()
    client = MongoClient()
    result = client.server_usage_reports.insert_one(doc)
    print(result)


