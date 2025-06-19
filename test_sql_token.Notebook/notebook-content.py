# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "jupyter",
# META     "jupyter_kernel_name": "python3.11"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "645da9b4-7bd7-41c8-a6b3-75175bc05216",
# META       "default_lakehouse_name": "lh_repro",
# META       "default_lakehouse_workspace_id": "5e92dfbe-4558-4e4b-9dca-c436930a0bd4",
# META       "known_lakehouses": [
# META         {
# META           "id": "645da9b4-7bd7-41c8-a6b3-75175bc05216"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

%pip install pyodbc

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

from notebookutils import credentials

token = credentials.getToken("pbi")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

import base64
import json

def base64url_decode(input_str):
    # Pad the string with '=' to make its length a multiple of 4
    rem = len(input_str) % 4
    if rem > 0:
        input_str += '=' * (4 - rem)
    return base64.urlsafe_b64decode(input_str)

header_b64, payload_b64, signature_b64 = token.split('.')
decoded_payload_json = base64url_decode(payload_b64).decode('utf-8')
payload = json.loads(decoded_payload_json)
print(token[2:]) # prepend ey ({) - otherwise output is redacted
print(payload)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

lh_name = notebookutils.runtime.context["defaultLakehouseName"]
lh_conn_str = notebookutils.lakehouse.getWithProperties(notebookutils.runtime.context["defaultLakehouseName"])["properties"]["sqlEndpointProperties"]["connectionString"]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

conn = ["DRIVER={ODBC Driver 18 for SQL Server}", f"SERVER={lh_conn_str}", f"Database={lh_name}"]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

from itertools import chain, repeat
import struct

def convert_access_token_to_mswindows_byte_string(token: str):
    value = bytes(token, "UTF-8")
    encoded_bytes = bytes(chain.from_iterable(zip(value, repeat(0))))
    return struct.pack("<i", len(encoded_bytes)) + encoded_bytes

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

sql_copt_ss_access_token = 1256
attrs_before = {sql_copt_ss_access_token: convert_access_token_to_mswindows_byte_string(token)}

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

import pyodbc

handle = pyodbc.connect(";".join(conn), attrs_before=attrs_before, autocommit=True)
with handle.cursor() as cursor:
    cursor.execute("select 'success' as result")
    res = cursor.fetchone()
    print(res[0])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }
