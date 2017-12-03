from pymongo import MongoClient


def main():
    client = MongoClient()
    db = client.utilize
    job_table = db.job_tracking_table
    

if __name__ == '__main__':
    main()
