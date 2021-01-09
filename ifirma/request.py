import hmac
import json
from binascii import unhexlify
from hashlib import sha1
import requests

from ifirma.config import API_USER, API_KEY
from ifirma.serializer import make_email, make_invoice

API_URL='https://www.ifirma.pl/iapi'
API_CREATE_INVOICE_URL = "{}/fakturakraj.json".format(API_URL)
API_SEND_EMAIL_URL_WITH_PARAM = "{}/fakturakraj/send/".format(API_URL), "{}.json?wyslijEfaktura=true"
API_GET_INVOICES_LIST_URL="{}/faktury.json".format(API_URL)
API_GET_INVOICE_DETAILS_URL_WITH_PARAM="{}/fakturakraj/".format(API_URL), "{}.json"
INVOICE_KEY_NAME = "faktura"

def sign_raw(data, key):
    api_key = key if isinstance(key, bytes) else unhexlify(key)
    bin_data = data.encode(encoding='utf-8', errors='strict')

    return hmac.new(api_key, bin_data, sha1).hexdigest()

def sign(request_url, data, api_user=None, api_key=None, api_scope=None):
    api_user, api_key, api_scope = api_user or API_USER, api_key or API_KEY, api_scope or INVOICE_KEY_NAME
    base_url = request_url.split('?')[0]

    sign_data = "{}{}{}{}".format(base_url, api_user, api_scope, data)
    api_token = sign_raw(sign_data, api_key)

    return "IAPIS user={}, hmac-sha1={}".format(api_user, api_token)

def send_invoice(invoice):
    json_req = json.dumps(make_invoice(invoice))
    auth = sign(API_CREATE_INVOICE_URL, json_req)
   
    headers = {'Content-Type': 'application/json; charset=utf8', 'Authentication': auth}
    r = requests.post(API_CREATE_INVOICE_URL, data=json_req, headers=headers)

    r.raise_for_status()
    return InvoiceResponse(r.json())

def send_email(invoice_id, email_address, text):
    json_req = json.dumps(make_email(email_address, text))
    url, param = API_SEND_EMAIL_URL_WITH_PARAM
    
    request_url = url + param.format(invoice_id)
    auth = sign(request_url, json_req)

    headers = {'Content-Type': 'application/json; charset=utf8', 'Authentication': auth}
    r = requests.post(request_url, data=json_req, headers=headers)

    r.raise_for_status()
    return r.json()

def get_invoices_list(date_from, date_to, invoice_type='prz_faktura_kraj', page=1, items_on_page=20):
    url = API_GET_INVOICES_LIST_URL

    request_url = url + "?typ={}&dataOd={}&dataDo={}&strona={}&iloscNaStronie={}".format(invoice_type, date_from, date_to, page, items_on_page)
    auth = sign(request_url, '')

    headers = {'Content-Type': 'application/json; charset=utf8', 'Authentication': auth}
    r = requests.get(request_url, headers=headers)

    r.raise_for_status()
    return r.json()

def get_invoice(invoice_id):
    url, param = API_GET_INVOICE_DETAILS_URL_WITH_PARAM

    request_url = url + param.format(invoice_id)
    auth = sign(request_url, '')

    headers = {'Content-Type': 'application/json; charset=utf8', 'Authentication': auth}
    r = requests.get(request_url, headers=headers)

    r.raise_for_status()
    return r.json()


class InvoiceResponse:
    def __init__(self, response):
        response = response['response']
        if not isinstance(response['Kod'], int):
            raise ValueError('Response in unsupported format')

        self.success = (response['Kod'] == 0)
        self.message = response['Informacja']
        if self.success:
            self.invoice_id = response['Identyfikator']
