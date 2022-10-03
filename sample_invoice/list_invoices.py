import os, sys
from datetime import date, timedelta
import requests
from pprint import pprint

script_path = os.path.realpath(__file__)
module_path = os.path.dirname(os.path.dirname(script_path))
sys.path.append(module_path)
print("Module path: " + module_path)

from ifirma.request import Request

if __name__ == "__main__":
    date_from = date(2022, 8, 1)
    params = dict(date_from=date_from, date_to=date_from + timedelta(days=30))
    req = Request().list(params)

    resp = req.execute(requests)
    resp.raise_for_status()
    invoices_json = resp.json()["response"]

    pprint(invoices_json)

    if invoices_json["Kod"] == 0 and invoices_json["Wynik"]:
        invoice_id = invoices_json["Wynik"][0]["FakturaId"]
        print(f"\nDetails of the invoice id: {invoice_id}\n")

        req = Request().get(invoice_id)
        resp = req.execute(requests)
        resp.raise_for_status()

        pprint(resp.json())
