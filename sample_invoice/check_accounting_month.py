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
import os, sys
import requests

script_path = os.path.realpath(__file__)
module_path = os.path.dirname(os.path.dirname(script_path))
sys.path.append(module_path)

from ifirma.request import Request, API_URL

req = Request(
	api_key_name="abonent", 
	api_key=os.environ.get("IFIRMA_abonent_API_KEY")
)
req.url = f"{API_URL}/abonent/miesiacksiegowy.json"

# Here the GET request method is used.
# `execute` only supports GET / POST requests
# For PUT one shall directly use of `requests` library
resp = req.execute(requests)

resp.raise_for_status()
invoices_json = resp.json()

print(invoices_json)
