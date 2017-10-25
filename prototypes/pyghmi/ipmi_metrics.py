from pyghmi.ipmi import command

ipmi = command.Command(bmc='eb2-2214-sd01ipmi.csc.ncsu.edu', userid='admin', password='sdteam18')
sensor = ipmi.get_sensor_reading('FAN1_SPEED')
print sensor
#sensors = ipmi.get_sensor_data()
#for s in sensors:
#	print s
