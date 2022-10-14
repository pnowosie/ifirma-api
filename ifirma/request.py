import json

INVOICE_KEY_NAME = "faktura"
API_URL = "https://www.ifirma.pl/iapi"
API_INVOICE_OPER = API_URL + "/fakturakraj"
API_INVOICE_LIST = API_URL + "/faktury.json"


class Request:
    def __init__(self, api_user=None, api_key=None, api_key_name=INVOICE_KEY_NAME):
        from ifirma.config import get_credentials

        self.data = None
        self.headers = {
            "Content-Type": "application/json; charset=utf8",
        }
        self.key_name = api_key_name
        self.api_user, self.api_key = get_credentials(api_user, api_key)

    def get(self, invoice_id):
        self.url = f"{API_INVOICE_OPER}/{invoice_id}.json"
        return self

    def email(self, invoice_id, data):
        self.data = Request.assert_data(data)
        self.url = f"{API_INVOICE_OPER}/send/{invoice_id}.json?wyslijEfaktura=true"
        return self

    def list(self, params):
        defaults = dict(invoice_type="prz_faktura_kraj", page=1, items_on_page=20)
        query = "?typ={invoice_type}&dataOd={date_from}&dataDo={date_to}&strona={page}&iloscNaStronie={items_on_page}"
        self.url = API_INVOICE_LIST + query.format(**{**defaults, **params})
        return self

    def download(self, invoice_id, print_type="single"):
        self.url = f"{API_INVOICE_OPER}/{invoice_id}.pdf.{print_type}"
        self.headers = {**self.headers, "Accept": "application/pdf"}
        return self

    def submit(self, data):
        self.data = Request.assert_data(data)
        self.url = f"{API_INVOICE_OPER}.json"
        return self

    @property
    def api_token(self):
        assert self.api_user, "Can't authenticate, missing api user"
        assert self.api_key, "Can't authenticate, missing api key"
        assert self.url, "Can't authenticate, missing url"

        base_url = self.url.split("?")[0]
        sign_data = f"{base_url}{self.api_user}{self.key_name}{self.data or ''}"

        return sign_raw(sign_data, self.api_key)

    @property
    def auth_header(self):
        return f"IAPIS user={self.api_user}, hmac-sha1={self.api_token}"

    def execute(self, http_module):
        headers = {**self.headers, "Authentication": self.auth_header}

        if self.data is not None:
            return http_module.post(self.url, data=self.data, headers=headers)
        else:
            return http_module.get(self.url, headers=headers)

    @staticmethod
    def assert_data(data):
        allowed_data_types = [dict, str]

        data_type_allowed = any(isinstance(data, type) for type in allowed_data_types)
        assert (
            data_type_allowed
        ), f"Data parameter has wrong type of '{type(data)}'. Data type should be {allowed_data_types}."

        if isinstance(data, str):
            data = json.loads(data)

        # we need to properly encode unicode characters in the string
        return json.dumps(data)


class InvoiceResponse:
    def __init__(self, response):
        response = response["response"]
        if not isinstance(response["Kod"], int):
            raise ValueError("Response in unsupported format")

        self.success = response["Kod"] == 0
        self.message = response["Informacja"]
        if self.success:
            self.invoice_id = response["Identyfikator"]

        # for tests when FakeHttpResponse.json() is passed
        if "_request" in response:
            self.test_data = response["_request"]

    def __repr__(self):
        return "InvoiceResponse(success=%r, %r)" % (
            self.success,
            self.invoice_id if self.success else self.message,
        )


def sign_raw(data, key):
    import hmac
    from binascii import unhexlify
    from hashlib import sha1

    api_key = key if isinstance(key, bytes) else unhexlify(key)
    bin_data = data.encode(encoding="utf-8", errors="strict")

    return hmac.new(api_key, bin_data, sha1).hexdigest()
