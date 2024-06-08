import os
import base64

secure_key = base64.b64encode(os.urandom(24)).decode('utf-8')
print(secure_key)
