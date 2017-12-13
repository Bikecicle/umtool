import pyipmi
import pyipmi.interfaces

interface = pyipmi.interfaces.create_interface('ipmitool', interface_type='lanplus')

connection = pyipmi.create_connection(interface)

connection.target = pyipmi.Target(0xb2)
connection.target.set_routing([(0x20,0)])

connection.session.set_session_type_rmcp('10.76.4.15', port=623)
connection.session.set_auth_type_user('admin', '/*hoRV7or2C')
connection.session.establish()

connection.get_device_id()
