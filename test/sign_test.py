import json
from ifirma.request import sign_raw, sign
from stubs import (
   SAMPLE_API_USER, 
   SEND_EMAIL_WITH_INVOICE_REQUEST
)

SAMPLE_API_KEY='EAB0D8ACF3308F3B'
API_SCOPE='faktura'

args = dict(api_user=SAMPLE_API_USER, api_key=SAMPLE_API_KEY, api_scope=API_SCOPE)

def test_sign():
    # example data from https://api.ifirma.pl/faq/
    assert '1558ab6c5ab2b0d1cd129b9ad11527cf33486705' == sign_raw('222222', b'111111')
    assert 'cec153ee6350475f117a307111e2bd7d83034925' == sign_raw('222222', '111111')

def test_sign_send_email_request():
    from ifirma.request import API_SEND_EMAIL_URL_WITH_PARAM

    json_to_sign = json.dumps(SEND_EMAIL_WITH_INVOICE_REQUEST)
    indented_json_to_sign = json.dumps(SEND_EMAIL_WITH_INVOICE_REQUEST, indent=2, sort_keys=True)
    url, param = API_SEND_EMAIL_URL_WITH_PARAM

    request_url = url + param.format(0)
    
    auth_header = sign(request_url, json_to_sign, **args)
    indented_auth_header = sign(request_url, indented_json_to_sign, **args)

    assert 'IAPIS user=jan.nowak@ifirma.pl, hmac-sha1=491bd26d7f487fb822007899183cf1a29de02f7a' == auth_header
    assert 'IAPIS user=jan.nowak@ifirma.pl, hmac-sha1=783a428f870a3bb0f70ed4cc78c3afd6bcaddd40' == indented_auth_header

def test_sign_get_invoices_list_request():
    from ifirma.request import API_GET_INVOICES_LIST_URL
    expected_header = 'IAPIS user=jan.nowak@ifirma.pl, hmac-sha1=081dec7098dbed6aab839e76501a964aa5b9386a'
    
    request_url = API_GET_INVOICES_LIST_URL
    request_url_with_params = request_url + '?strona=5&iloscNaStronie=7'

    auth_header = sign(request_url, '', **args)
    auth_header_with_params = sign(request_url_with_params, '', **args)

    # signature does not depends on params
    assert expected_header == auth_header
    assert expected_header == auth_header_with_params

def test_sign_get_invoice_details_request():
    from ifirma.request import API_GET_INVOICE_DETAILS_URL_WITH_PARAM
    
    url, param = API_GET_INVOICE_DETAILS_URL_WITH_PARAM
    request_url = url + param.format(1337)

    auth_header = sign(request_url, '', **args)

    assert 'IAPIS user=jan.nowak@ifirma.pl, hmac-sha1=40600699c8f72e4165b11f98c4cb93253a3cc7dc' == auth_header


SAMPLE_DATA_DIR = './test/data'
from ifirma.request import API_CREATE_INVOICE_URL

def test_sign_create_vat_payer_invoice_with_known_customer_request():
    payload = open(f'{SAMPLE_DATA_DIR}/create_vat_payer_invoice_with_known_customer.request.json').read()

    auth_header = sign(API_CREATE_INVOICE_URL, payload, **args)
    
    assert 'IAPIS user=jan.nowak@ifirma.pl, hmac-sha1=33443d8492027e0fb549f4d4aeed48cc5891cf2f' == auth_header

def test_sign_create_vat_payer_invoice_with_new_customer_request():
    payload = open(f'{SAMPLE_DATA_DIR}/create_vat_payer_invoice_with_new_customer.request.json').read()

    auth_header = sign(API_CREATE_INVOICE_URL, payload, **args)
    
    assert 'IAPIS user=jan.nowak@ifirma.pl, hmac-sha1=418cea6c93f4deadbeb5a5e9b25f63145db6a9c0' == auth_header

def test_sign_create_nonvat_payer_invoice_with_new_customer_request():
    payload = open(f'{SAMPLE_DATA_DIR}/create_nonvat_payer_invoice_with_new_customer.request.json').read()

    auth_header = sign(API_CREATE_INVOICE_URL, payload, **args)
    
    assert 'IAPIS user=jan.nowak@ifirma.pl, hmac-sha1=c2d3a2c69988792b2941336a3059dc035253407d' == auth_header

def test_sign_create_nonvat_payer_invoice_with_known_customer_request():
    payload = open(f'{SAMPLE_DATA_DIR}/create_nonvat_payer_invoice_with_known_customer.request.json').read()

    auth_header = sign(API_CREATE_INVOICE_URL, payload, **args)
    
    assert 'IAPIS user=jan.nowak@ifirma.pl, hmac-sha1=ec0b955b8e63733ecb6ebd461d0783391c09bce1' == auth_header