"""
A thin service layer (incomplete functionality covered)

Even if it does not directly require any specific implementation
of:
- serializer module
- http module

It depends on it's API, e.g. requests.Response is expected to be
returned from `Request.execute()` or expects `file_handle` would
implement pathlib.Path.write_bytes()

"""
import json

import ifirma.config as Config
from ifirma.invoice import Invoice
from ifirma.request import Request


def create_invoice(invoice):
    from ifirma.request import InvoiceResponse

    http = Config.get_http_module()

    data = _serialize(invoice)
    resp = Request().submit(data).execute(http)

    resp.raise_for_status()
    return InvoiceResponse(resp.json())


def email_invoice(invoice_id, email_addr, message):
    serializer = Config.get_serializer_module()
    http = Config.get_http_module()

    data = serializer.make_email(email_addr, message)
    resp = Request().email(invoice_id, data).execute(http)

    resp.raise_for_status()
    return resp.json()


def download_invoice(invoice_id, file_handle):
    http = Config.get_http_module()

    resp = Request().download(invoice_id).execute(http)

    resp.raise_for_status()
    file_handle.write_bytes(resp.content)


def _serialize(invoice_kind):
    if not isinstance(invoice_kind, Invoice):
        return invoice_kind

    serializer = Config.get_serializer_module()
    return serializer.make_invoice(invoice_kind)
