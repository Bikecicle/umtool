# coding=utf-8
""" Simple example to use python-redfish on HP Proliant servers """
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
from builtins import str

import os
import sys
import json
import redfish
import urllib3
standard_library.install_aliases()

# Disable certificate warnings - this should be handled more gracefully down the road
urllib3.disable_warnings()

# Get $HOME environment.
HOME = os.getenv('HOME')

if HOME == '':
    print("$HOME environment variable not set, please check your system")
    sys.exit(1)

try:
    with open(HOME + "/.redfish/inventory") as json_data:
        config = json.load(json_data)
        json_data.close()
except IOError as e:
    print("Please create a json configuration file")
    print(e)
    sys.exit(1)

URL = config["Managers"]["team"]["url"]
USER_NAME = config["Managers"]["team"]["login"]
PASSWORD = config["Managers"]["team"]["password"]

''' remote_mgmt is a redfish.RedfishConnection object '''
try:
    remote_mgmt = redfish.connect(URL,
                                  USER_NAME,
                                  PASSWORD,
                                  simulator=False,
                                  verify_cert=False)
except redfish.exception.RedfishException as e:
    sys.stderr.write(str(e.message))
    sys.stderr.write(str(e.advices))
    sys.exit(1)

print ("Redfish API version : %s \n" % remote_mgmt.get_api_version())

# Uncomment following line to reset the blade !!!
# remote_mgmt.Systems.systems_dict["1"].reset_system()

print("Bios version : {}\n".format(
    remote_mgmt.Systems.systems_dict["1"].get_bios_version()))
print("Serial Number : {}\n".format(
    remote_mgmt.Systems.systems_dict["1"].get_serial_number()))
print("Power State : {}\n".format(
    remote_mgmt.Systems.systems_dict["1"].get_power()))
print("Parameter 'SystemType' : {}\n".format(
    remote_mgmt.Systems.systems_dict["1"].get_parameter("SystemType")))

print("Get bios parameters : {}\n".format(
    remote_mgmt.Systems.systems_dict["1"].bios.get_parameters()))
print("Get boot parameters : {}\n".format(
    remote_mgmt.Systems.systems_dict["1"].bios.boot.get_parameters()))

mySystem = remote_mgmt.Systems.systems_dict["1"]
mySystem.set_boot_source_override("None", "Disabled")
# Uncomment the next line to reset the server
# mySystem.reset_system()


print("Get manager firmware version : {}\n".format(
    remote_mgmt.Managers.managers_dict["1"].get_firmware_version()))
print("Get system Bios version : {}\n".format(
    remote_mgmt.Systems.systems_dict["1"].get_bios_version()))

# Reset of the system is required to apply the changes
# remote_mgmt.Systems.systems_dict["1"].reset_system()

remote_mgmt.logout()
