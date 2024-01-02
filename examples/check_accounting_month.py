"""
Example shows how to use this package to authenticate requests 
from others ifirma's API sections than "faktura".

Set env variable of name `IFIRMA_abonent_API_KEY` with the value
of the approriate key.

USAGE:
$ export IFIRMA_abonent_API_KEY=EAB0D8ACF3308F3B
$ python sample_invoice/check_accounting_month.py

Please note that `api_key_name` is not fully supported and then
you need to provide the API key manually. Otherwise value of
environment variable of `IFIRMA_API_KEY` will be used.

# IMPORTANT: This example requires that "abonent" API key is generated.
# See ifirma's "Podstawowe klucze autoryzacji" in the "Settings / API" section
"""
import os, sys, json
import requests

script_path = os.path.realpath(__file__)
module_path = os.path.dirname(os.path.dirname(script_path))
sys.path.append(module_path)

from ifirma.request import Request, API_URL

req = Request(api_key_name="abonent", api_key=os.environ.get("IFIRMA_abonent_API_KEY"))
req.url = f"{API_URL}/abonent/miesiacksiegowy.json"

if len(sys.argv) > 1:
    if sys.argv[1] not in ["NAST", "POPRZ"]:
        print("USAGE: python check_accounting_month.py [opt: `POPRZ | NAST`]")
        sys.exit(
            "Run without args to check current month. Provide 'NAST' or 'POPRZ' to change."
        )
    # Here the PUT request method is used.
    # Because `req.execute` only supports GET / POST requests
    # for PUT one shall directly use of `requests` library
    req.data = json.dumps(
        dict(MiesiacKsiegowy=sys.argv[1], PrzeniesDaneZPoprzedniegoRoku=False)
    )
    headers = {**req.headers, "Authentication": req.auth_header}
    resp = requests.put(req.url, data=req.data, headers=headers)
    print(resp.json())

    req.data = None

# Checking the current accounting month
resp = req.execute(requests)

resp.raise_for_status()
resp_json = resp.json()

print(resp_json)
