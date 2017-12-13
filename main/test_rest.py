#! /usr/bin/env python
from __future__ import print_function
import requests

def main():
    print("Test 1")
    test_1()
    print("Test 2")
    test_2()
    print("Test 3")
    test_1()


def test_1():
    addr = 'http://localhost:8080/list_jobs'

    r = requests.get(addr)

    print(r)
    

def test_2():
    data = {'interval':3,
            'hosts':[{'hostname':'eb2-2214-sd01ipmi.csc.ncsu.edu', 'username':'admin','password':'sdteam18','unique_id':'MAC'}]
    }

    addr = 'http://localhost:8080/start_job'

    r = requests.post(addr, data)

    print(r)

if __name__ == "__main__":
    main()

