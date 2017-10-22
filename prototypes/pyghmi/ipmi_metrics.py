from pyghmi.ipmi import command

ipmi = command.Command(bmc='eb2-2214-sd01ipmi.csc.ncsu.edu', userid='admin', password='sdteam18')
sensors = ipmi.get_sensor_data()
for s in sensors:
	print s
