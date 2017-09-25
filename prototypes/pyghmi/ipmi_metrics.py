from pyghmi.ipmi import command

ipmi = command.Command(bmc='eb2tvx02drac.csc.ncsu.edu', userid='admin', password='/*hoRV7or2C')
sensors = ipmi.get_sensor_descriptions()
for s in sensors:
	print s
