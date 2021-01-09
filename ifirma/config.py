import os

API_USER=os.environ.get('IFIRMA_API_USERNAME', '<username>')
API_KEY=os.environ.get('IFIRMA_API_KEY', 'API_KEY')

INVOICE_ISSUER=None
INVOICE_PLACE=None

def configure(issuer=None, place=None):
    global INVOICE_ISSUER, INVOICE_PLACE
    INVOICE_ISSUER=issuer
    INVOICE_PLACE=place
