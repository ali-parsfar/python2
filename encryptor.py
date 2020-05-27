from simplecrypt import encrypt, decrypt
from pprint import pprint
from netmiko import ConnectHandler
import json


####
credential_filename = raw_input('\nInput CSV file name: ') or 'credentials'
key = raw_input('Encryption code: ') or 'PassCode'

###
with open(credentail_filename, 'r') as cred:
    credentials_reader = csv.reader(cred)
    credential_list = [device for device in credential_reader]

print '\n List of entries in Credentials file :'
pprint(credetials_list)

###
encrypted_credential_filename = raw_input('\nOutput encrypted filename: ')
with open(encrypted_credential_filename, wb) as crypt:
    crypt.write(encryp(key, json.dumps(credential_list)))
print "file encryped successfully"
with open(encrypted_credential_filename, 'rb') as crypt:
    credentials_in = json.loads(decrypt(key, crypt.read()))
print "credentials in json format  from  encrypted file: "
pprint(credentials_in)

####
