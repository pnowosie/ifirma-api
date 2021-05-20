from ifirma.request import Request
from fake_http_module import GET, POST, FakeHttpModule

def test_get_invoice_details_url():
    res = Request().get(invoice_id=1337).execute(FakeHttpModule)
    assert (GET, "https://www.ifirma.pl/iapi/fakturakraj/1337.json") == get_url(res)

def test_list_invoices_url():
    from datetime import date, timedelta
    df = date(1970, 1, 1)
    dt = df + timedelta(days=30)

    req = Request().list(params=dict(date_from=df, date_to=dt, page=7))
    res = req.execute(FakeHttpModule)

    assert req.data is None
    assert (GET,
        "https://www.ifirma.pl/iapi/faktury.json?typ=prz_faktura_kraj"
        "&dataOd=1970-01-01&dataDo=1970-01-31&strona=7&iloscNaStronie=20"
    ) == get_url(res)

def test_invoice_download_url():
    res = Request().download(invoice_id=1337, print_type='dup').execute(FakeHttpModule)
    assert (GET, "https://www.ifirma.pl/iapi/fakturakraj/1337.pdf.dup") == get_url(res)

def test_send_invoice_email_url():
    res = Request().email(invoice_id=1337, data=dict()).execute(FakeHttpModule)
    assert (POST, "https://www.ifirma.pl/iapi/fakturakraj/send/1337.json?wyslijEfaktura=true") == get_url(res)

def test_submit_invoice_url():
    res = Request().submit(data=dict()).execute(FakeHttpModule)
    assert (POST, "https://www.ifirma.pl/iapi/fakturakraj.json") == get_url(res)

def get_url(exec_result):
    method, url, *_ = exec_result
    print(f"get_url Method: {method}")
    return method, url