import os
import sys
from pathlib import Path

from ifirma import api

USAGE = 'USAGE: py download_invoice.py <invoice_id> <download_dir>'
if __name__ == "__main__":

    if len(sys.argv) < 3:
        sys.exit(USAGE)

    invoice_id = sys.argv[1]
    download_dir = Path(sys.argv[2])

    if not download_dir.exists():
        sys.exit(f"ERROR: Path '{download_dir}' does not exists")

    path = download_dir / f"invoice_{invoice_id}.pdf"
    api.download_invoice(invoice_id, Path(path))
    print(f"File written to {path}")
