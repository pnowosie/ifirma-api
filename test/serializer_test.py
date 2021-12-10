from ifirma.invoice import INVOICE_TYPE
from ifirma.serializer import make_invoice
from stubs import (
  INVOICE_WITH_KNOWN_CUSTOMER,
  PAYED_INVOICE_WITH_NEW_CUSTOMER,
  SEND_EMAIL_WITH_INVOICE_REQUEST,
  PAYED_NONVAT_INVOICE_FOR_COMPANY,
)
from json import dumps

SAMPLE_DATA_DIR = './test/data'


def test_create_vat_payer_invoice_with_known_customer_request():
    EXPECTED_INVOICE_REQ = open(f'{SAMPLE_DATA_DIR}/create_vat_payer_invoice_with_known_customer.request.json').read()
    INVOICE_WITH_KNOWN_CUSTOMER.invoice_type = INVOICE_TYPE.VAT_PAYER
    assert EXPECTED_INVOICE_REQ == dumps(make_invoice(INVOICE_WITH_KNOWN_CUSTOMER), indent=2, sort_keys=True)

def test_create_vat_payer_invoice_with_new_customer_request():
    EXPECTED_INVOICE_REQ = open(f'{SAMPLE_DATA_DIR}/create_vat_payer_invoice_with_new_customer.request.json').read()
    PAYED_INVOICE_WITH_NEW_CUSTOMER.invoice_type = INVOICE_TYPE.VAT_PAYER
    assert EXPECTED_INVOICE_REQ == dumps(make_invoice(PAYED_INVOICE_WITH_NEW_CUSTOMER), indent=2, sort_keys=True)

def test_create_nonvat_payer_invoice_with_new_customer_request():
    EXPECTED_INVOICE_REQ = open(f'{SAMPLE_DATA_DIR}/create_nonvat_payer_invoice_with_new_customer.request.json').read()
    PAYED_INVOICE_WITH_NEW_CUSTOMER.invoice_type = INVOICE_TYPE.NON_VAT_PAYER
    assert EXPECTED_INVOICE_REQ == dumps(make_invoice(PAYED_INVOICE_WITH_NEW_CUSTOMER), indent=2, sort_keys=True)

def test_create_nonvat_payer_invoice_with_known_customer_request():
    EXPECTED_INVOICE_REQ = open(f'{SAMPLE_DATA_DIR}/create_nonvat_payer_invoice_with_known_customer.request.json').read()
    INVOICE_WITH_KNOWN_CUSTOMER.invoice_type = INVOICE_TYPE.NON_VAT_PAYER
    assert EXPECTED_INVOICE_REQ == dumps(make_invoice(INVOICE_WITH_KNOWN_CUSTOMER), indent=2, sort_keys=True)

def test_send_email_with_invoice_request():
    EXPECTED_EMAIL_REQ = open(f'{SAMPLE_DATA_DIR}/send_email_with_invoice.request.json').read()
    assert EXPECTED_EMAIL_REQ == dumps(SEND_EMAIL_WITH_INVOICE_REQUEST, indent=2, sort_keys=True)

def test_create_nonvat_payer_invoice_with_new_company_customer_request():
    EXPECTED_INVOICE_REQ = open(f'{SAMPLE_DATA_DIR}/create_nonvat_payer_invoice_with_new_company_customer.request.json').read()
    PAYED_NONVAT_INVOICE_FOR_COMPANY.invoice_type = INVOICE_TYPE.NON_VAT_PAYER
    generated_invoice_req = dumps(make_invoice(PAYED_NONVAT_INVOICE_FOR_COMPANY), indent=2, sort_keys=True)
    #print(generated_invoice_req)
    assert EXPECTED_INVOICE_REQ == generated_invoice_req
