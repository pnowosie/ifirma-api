import os
import sys
from pathlib import Path

script_path = os.path.realpath(__file__)
module_path = os.path.dirname(os.path.dirname(script_path))
sys.path.append(module_path)
print("Module path: " + module_path)

from ifirma.yaml_parser import parse
import ifirma.api as Api


if __name__ == "__main__":
    if len(sys.argv) == 1 or not sys.argv[1].strip():
        sys.exit('Provide a yaml file name containing the invoice')
    else:
        filename = sys.argv[1]
        print('Reading file: ' + filename)

    with open(filename) as f:
        task = parse(f)

    create_invoice_response = Api.create_invoice(task['invoice'])
    invoice_id = create_invoice_response.invoice_id

    print(f'Invoice created successfully {create_invoice_response}')

    if create_invoice_response.success and (email_address := task.get('send_to')):
        email_send_response = Api.email_invoice(invoice_id, email_address, task['message'])
        print(f'Email sent {email_send_response}')

    if create_invoice_response.success and (download_dir := task.get('download')):
        download_path = Path(download_dir) / f"invoice_{invoice_id}.pdf"
        Api.download_invoice(invoice_id, download_path)
        print(f"Invoice written to {download_path}")
