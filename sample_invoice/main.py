import os, sys
import requests
from pathlib import Path


temp_dir = Path("/tmp")
script_path = os.path.realpath(__file__)
module_path = os.path.dirname(os.path.dirname(script_path))
sys.path.append(module_path)
print("Module path: " + module_path)

from ifirma.yaml_parser import parse
from ifirma.serializer import make_email, make_invoice
from ifirma.request import Request, InvoiceResponse



if __name__ == "__main__":
    if len(sys.argv) == 1 or not sys.argv[1].strip():
        sys.exit('Provide a yaml file name containing the invoice')
    else:
        filename = sys.argv[1]
        print('Reading file: ' + filename)

    with open(filename) as f:
        task = parse(f)
    
    invoice_data = make_invoice(task['invoice'])
    submit_reqest = Request().submit(invoice_data)
    resp = submit_reqest.execute(requests)
    resp.raise_for_status()
    create_invoice_response = InvoiceResponse(resp.json())
    print(create_invoice_response)
    invoice_id = create_invoice_response.invoice_id

    print(f'Invoice created successfully {invoice_id=}')

    if create_invoice_response.success and (email_address := task.get('send_to')):
        email_data = make_email(email_address, task['message'])
        email_request = Request().email(invoice_id, email_data)
        email_send_response = email_request.execute(requests)
        email_send_response.raise_for_status()
        print(f'Email sent {email_send_response.json()}')

    download_path = temp_dir / f"invoice_{invoice_id}.pdf"
    download_request = Request().download(invoice_id)
    download_resp = download_request.execute(requests)
    download_resp.raise_for_status()

    download_path.write_bytes(download_resp.content)
    print(f"Invoice written to {download_path}")
