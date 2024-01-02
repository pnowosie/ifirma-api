"""
Example shows how to use this package to authenticate 
and send other invoice type than this package natively supports.

Request to send: sample_invoice/arbitrary_other_invoice_type.json
which is "Świadczenie usług poza terytorium kraju"

USAGE:
$ python sample_invoice/send_arbitrary_other_requests.py
"""
import os, sys
from pathlib import Path

script_path = os.path.realpath(__file__)
module_path = os.path.dirname(os.path.dirname(script_path))
sys.path.append(module_path)

from ifirma.api import create_invoice, download_invoice
from src import ifirma as url_mod

if __name__ == "__main__":
    filename = "sample_invoice/arbitrary_other_invoice_type.json"
    print("Reading file: " + filename)

    file_content = open(filename, encoding="utf-8").read()

    url_mod.API_INVOICE_OPER = url_mod.API_URL + "/fakturaeksportuslug"
    resp = create_invoice(file_content)
    print(resp)

    # and download it
    invoice_id = resp.invoice_id
    path = f"invoice_{invoice_id}.pdf"
    download_invoice(invoice_id, Path(path))
