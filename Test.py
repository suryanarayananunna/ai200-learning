

import json


try:
    value = 10 / 0
except Exception as e:
    print(f"Error: {e}")
finally:
    print("Execution completed.")


py_dist = '{    "azure-identity": "1.12.0",    "status": true}'

json_dist = json.loads(py_dist)
print(json_dist)