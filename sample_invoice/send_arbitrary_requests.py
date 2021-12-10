"""
Example shows how to use this package to authenticate 
arbitrary request from json file.

USAGE:
$ python sample_invoice/send_arbitrary_requests.py <PATH TO REQUEST.json>
"""
import os, sys
import requests

script_path = os.path.realpath(__file__)
module_path = os.path.dirname(os.path.dirname(script_path))
sys.path.append(module_path)

from ifirma.request import Request

if __name__ == "__main__":
    if len(sys.argv) == 1 or not sys.argv[1].strip():
        sys.exit('Provide an ifirma invoice request json')
    else:
        filename = sys.argv[1]
        print('Reading file: ' + filename)

    file_content = open(filename).read()
    req = Request()
    resp = req.submit(file_content).execute(requests)

    resp.raise_for_status()
    invoices_json = resp.json()
    print(invoices_json)
