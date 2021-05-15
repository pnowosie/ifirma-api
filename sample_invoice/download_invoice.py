import os, sys
import requests
from pathlib import Path

script_path = os.path.realpath(__file__)
module_path = os.path.dirname(os.path.dirname(script_path))
sys.path.append(module_path)
print("Module path: " + module_path)

from ifirma.request import Request

USAGE = 'USAGE: python download_invoice.py <invoice_id> <download_dir>'
if __name__ == "__main__":

    if len(sys.argv) < 3:
        sys.exit(USAGE)

    invoice_id = sys.argv[1]
    download_dir = Path(sys.argv[2])

    if not download_dir.exists():
        sys.exit(f"ERROR: Path '{download_dir}' does not exists")

    req = Request().download(invoice_id)
    resp = req.execute(requests)
    resp.raise_for_status()

    path = download_dir / f"invoice_{invoice_id}.pdf" 
    path.write_bytes(resp.content)

    print(f"File written to {path}")
