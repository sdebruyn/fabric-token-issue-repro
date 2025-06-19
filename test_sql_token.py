import base64
import json
from itertools import chain, repeat
import struct
import pyodbc
from azure.identity import ClientSecretCredential

lh_name = "lh_repro"  # TODO: fill in your Lakehouse name here
lh_conn_str = "TODO.datawarehouse.fabric.microsoft.com"  # TODO: fill in your connection string here

cred = ClientSecretCredential(
    tenant_id="TODO",  # TODO: fill in your tenant ID here
    client_id="TODO",  # TODO: fill in your client ID here
    client_secret="TODO",  # TODO: fill in your client secret here
)

token = cred.get_token("https://analysis.windows.net/powerbi/api/.default").token


def convert_access_token_to_mswindows_byte_string(token: str):
    value = bytes(token, "UTF-8")
    encoded_bytes = bytes(chain.from_iterable(zip(value, repeat(0))))
    return struct.pack("<i", len(encoded_bytes)) + encoded_bytes


def base64url_decode(input_str):
    # Pad the string with '=' to make its length a multiple of 4
    rem = len(input_str) % 4
    if rem > 0:
        input_str += "=" * (4 - rem)
    return base64.urlsafe_b64decode(input_str)


header_b64, payload_b64, signature_b64 = token.split(".")
decoded_payload_json = base64url_decode(payload_b64).decode("utf-8")
payload = json.loads(decoded_payload_json)
print(token)
print(payload)

conn = [
    "DRIVER={ODBC Driver 18 for SQL Server}",
    f"SERVER={lh_conn_str}",
    f"Database={lh_name}",
]

sql_copt_ss_access_token = 1256
attrs_before = {
    sql_copt_ss_access_token: convert_access_token_to_mswindows_byte_string(token)
}

handle = pyodbc.connect(";".join(conn), attrs_before=attrs_before, autocommit=True)
with handle.cursor() as cursor:
    cursor.execute("select 'success' as result")
    res = cursor.fetchone()
    print(res[0])
