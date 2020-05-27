
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from simplecrypt import encrypt, decrypt
from pprint import pprint
import json


###### Functions: ########

def read_devices(devices_filename):


device = {}
with open(devices_filename) as devices_filename:
    for device_line in devices_file:
        device_info = device_line.strip().splite(',')
        device = {
            'ipaddr': device_info[0],
            'type': device_info[1],
            'name': device_info[2]
        }
        devices[device['ipaddr']] = device
        print '\n----- devices -------------------'
        pprint(devices)
        return devices
##


def read_device_creds(device_creds_filename, key):
    print '\n----- getting credentials -----\n'
    with open(device_creds_filename, 'rb') as device_creds_filename:
        device_creds_json = decrypt(key, device_creds_filename.read())
    device_creds_list = json.loads(device_creds_json)
    pprint(device_creds_list)
    print '\n----- device_creds ------------------'
    device_creds = {dev[0]: dev for dev in device_creds_list}
    pprint(device_creds)
    return device_creds
##


def config_worker(device, creds):
    if device['type'] == 'syd_dmz':
        device_type = 'sydney_cisco_dmz_switch'
    elif device['type'] == 'syd-sw':
        device_type = 'sydney_cisco_int_switch'
    elif device['type'] == 'syd_wap':
        device_type = 'sydney_cisco_wap'
    else:
        device_type = 'cisco_ios'


print ' ----- connecting to device={0}, username={1} '
try:
    session = ConnectHandler(device_type='cisco_ios',
                             ip=device['ipaddr'],
                             username=creds[1],
                             password=creds[2]
                             )
#   session = ConnectHandler(device_type='cisco_ios', ip=192.168.1.201, usename='test', password='test')
    except (AuthenticationException):
    print 'Authentication Failure: ' + device['ipaddr']
    continue
except (NetMikoTimeoutException):
    print 'Timeout to device: ' + device['ipaddr']
    continue
except (EOFError):
    print 'End of file while attemting device : ' + device['ipaddr']
    continue
except (SSHExecution):
    print 'SSH Issue, is ssh enable on device : ' + device['ipaddr']
    continue
except Exception as unknown_error:
    print 'Unknown error on device : ' + device['ipaddr']
    continue
if device_type == 'syd_wap':
    print '---- Sydney office wap: ' + device['ipaddr']
    with open('commands_file'_syd_dmz) as f:
    commands_list = f.read().splitlines()
    output = session.send_command(command_list)
    print output

if device_type == 'syd_dmz':
    print '---- Sydney office dmz: ' + device['ipaddr']
    with open('commands_file'_syd_dmz) as f:
    commands_list = f.read().splitlines()
    output = session.send_command(command_list)
    print output

if device_type == 'syd_sw':
    print '---- Sydney office int switch: ' + device['ipaddr']
    with open('commands_file'_syd_sw) as f:
    commands_list = f.read().splitlines()
    output = session.send_command(command_list)
    print output

    session.disconnect()
    return


######## Main ######
devices = read_devices('devices-file')
creds = read_device_creds('encrypt-device-creds', 'PassCode')

####
print '\n----- Begin ------\n'
for ipaddr, device in devices.items():
    print 'Getting config for:', device
    config_worker(device, creds[ipaddr])
print '\n----- End ----\n'
####
