GET = 'GET'
POST = 'POST'


class FakeHttpModule:
    @staticmethod
    def get(url, headers):
        print("FakeHttpModule Method: GET")
        return GET, url, headers


    @staticmethod
    def post(url, data, headers):
        print("FakeHttpModule Method: POST")
        return POST, url, headers, data
