from pymongo import MongoClient

def main():
    client = MongoClient()
    db = client.utilize
    report_table = db.usage_report_table
    reports = report_table.find()

    rows = []
    for report in reports:
        readings = report['readings']

        row = [str(report['timestamp'])]
        for reading in readings:
            name = reading['name']
            value = reading['value']
            if value is not None and value > 0:
                #print("'{}' NUMERIC,".format(name, value))
                row.append(str(value))
                #print("'{}' NUMERIC,".format(name, value))
        rowstring = ",".join(row)
        rows.append(rowstring)

    with open('myfile.csv', 'w') as myfile:
        myfile.write("\n".join(rows))

if __name__ == '__main__':
    main()
