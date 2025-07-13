#!/usr/bin/python3

import base64

data = 'QI6V2AAAYQLFjpI2BNXVB++QDezmSzUVss8wurdFA+/0zfTzDvI='
payload = base64.b64decode(data)
hexstr = ["%02x" %x for x in payload]
print(''.join(hexstr))
