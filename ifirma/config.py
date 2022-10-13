import os

INVOICE_ISSUER = None
INVOICE_PLACE = None


def configure(issuer=None, place=None):
    global INVOICE_ISSUER, INVOICE_PLACE
    INVOICE_ISSUER = issuer
    INVOICE_PLACE = place


def get_credentials(api_user=None, api_key=None):
    return (
        api_user or os.environ.get("IFIRMA_API_USERNAME", "<username>"),
        api_key or os.environ.get("IFIRMA_API_KEY", b"APIKEY"),
    )


HttpModule = None
SerializerModule = None


def get_http_module():
    import requests

    return HttpModule or requests


def get_serializer_module():
    import ifirma.serializer as Serializer

    return SerializerModule or Serializer
