import os
import time
from pyghmi.ipmi import command

tsum = 0
count = 10

ipmi = command.Command(bmc='eb2-2214-sd01ipmi.csc.ncsu.edu', userid='admin', password='sdteam18')

for i in range(count):
	ts = int(round(time.time() * 1000))
	sensor = ipmi.get_sensor_reading('FAN1_SPEED')
	print sensor
	te = int(round(time.time() * 1000))
	tsum += te - ts

print tsum/count
