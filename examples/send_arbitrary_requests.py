"""
Example shows how to use this package to authenticate 
arbitrary request from json file.

USAGE:
$ py send_arbitrary_requests.py <PATH TO REQUEST.json>
"""
import os, sys

from ifirma.api import create_invoice

if __name__ == "__main__":
    if len(sys.argv) == 1 or not sys.argv[1].strip():
        sys.exit("Provide an ifirma invoice request json")
    else:
        filename = sys.argv[1]
        print("Reading file: " + filename)

    file_content = open(filename, encoding="utf-8").read()
    resp = create_invoice(file_content)

    print(resp)
