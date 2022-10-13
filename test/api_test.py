import ifirma.api as api
from fake_http_module import FakeHttpModule
import ifirma.config as config
from stubs import INVOICE_WITH_KNOWN_CUSTOMER
import json, pytest

config.HttpModule = FakeHttpModule

SAMPLE_DATA_DIR = "./test/data"

sample_invoice = INVOICE_WITH_KNOWN_CUSTOMER
sample_invoice_request = open(
    f"{SAMPLE_DATA_DIR}/create_vat_payer_invoice_with_known_customer.request.json"
).read()


def test_create_invoice_with_invoice_object():
    resp = create_invoice(sample_invoice)

    # sanity check as FakeHttpResponse always render successful response
    assert resp.success, "Response isn't successful"


def test_create_invoice_serializes_invoice_object():
    resp = create_invoice(sample_invoice)

    post, _url, _hdr, payload = resp.test_data
    assert post == "POST", f"Unexpected request method {post}"
    assert isinstance(payload, str)
    assert sample_invoice_request == payload


def test_create_invoice_accepts_arbitrary_ifirma_request():
    resp = create_invoice(sample_invoice_request)

    payload = resp.test_data[3]

    # request stays the same
    assert sample_invoice_request == payload


def test_create_invoice_properly_escapes_nonascii_in_request():
    pl_dictricts_req = open(
        f"{SAMPLE_DATA_DIR}/create_vat_payer_invoice_with_known_customer.request.pl.json"
    ).read()

    resp = create_invoice(pl_dictricts_req)

    payload = resp.test_data[3]
    assert sample_invoice_request == payload


def test_create_invoice_accepts_json_request():
    pl_dictricts_req = open(
        f"{SAMPLE_DATA_DIR}/create_vat_payer_invoice_with_known_customer.request.pl.json"
    ).read()
    json_req = json.loads(pl_dictricts_req)
    assert type(json_req) == dict

    resp = create_invoice(json_req)

    payload = resp.test_data[3]
    assert sample_invoice_request == payload


def create_invoice(invoice_kind):
    resp = api.create_invoice(invoice_kind)
    clean_request_payload_data(resp)
    return resp


def clean_request_payload_data(resp):
    json_data = json.loads(resp.test_data[3])
    proper_json_text = json.dumps(json_data, indent=2, sort_keys=True)
    resp.test_data = (*resp.test_data[:3], proper_json_text)
