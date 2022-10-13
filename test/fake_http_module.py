GET = "GET"
POST = "POST"


class FakeHttpModule:
    @staticmethod
    def get(url, headers):
        print("FakeHttpModule Method: GET")
        return FakeHttpResponse((GET, url, headers))

    @staticmethod
    def post(url, data, headers):
        print("FakeHttpModule Method: POST")
        return FakeHttpResponse((POST, url, headers, data))


class FakeHttpResponse:
    def __init__(self, req_tuple) -> None:
        self.method, self.url, self.headers = req_tuple[:3]
        self.data = req_tuple[3] if len(req_tuple) > 3 else None

    def raise_for_status(self):
        # Fake is always successful
        pass

    def json(self):
        response = {
            "Kod": 0,
            "Informacja": f"Fake Response ({self.method, self.url})",
            "Identyfikator": "123123.fake",
            "_request": (self.method, self.url, self.headers, self.data),
        }
        return dict(response=response)

    def __iter__(self):
        """To be able to unpack response e.g. `method, url, header = response`"""
        yield self.method
        yield self.url
        yield self.headers
        if self.data:
            yield self.data

    def __getitem__(self, item):
        """To be able to subscript the response, e.g. obj `response[1]`"""
        return (self.method, self.url, self.headers, self.data)[item]
