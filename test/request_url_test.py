from ifirma.request import Request

def test_get_invoice_details_url():
    req = Request().get(invoice_id=1337)
    assert req.url == "https://www.ifirma.pl/iapi/fakturakraj/1337.json"

def test_list_invoices_url():
    from datetime import date, timedelta
    df = date(1970, 1, 1)
    dt = df + timedelta(days=30)

    req = Request().list(params=dict(date_from=df, date_to=dt, page=7))
    assert (req.url == 
        "https://www.ifirma.pl/iapi/faktury.json?typ=prz_faktura_kraj"
        "&dataOd=1970-01-01&dataDo=1970-01-31&strona=7&iloscNaStronie=20"
    )

def test_invoice_download_url():
    req = Request().download(invoice_id=1337, print_type='dup')
    assert req.url == "https://www.ifirma.pl/iapi/fakturakraj/1337.pdf.dup"

def test_send_invoice_email_url():
    req = Request().email(invoice_id=1337, data=dict())
    assert req.url == "https://www.ifirma.pl/iapi/fakturakraj/send/1337.json?wyslijEfaktura=true"

def test_submit_invoice_url():
    req = Request().submit(data=dict())
    assert req.url == "https://www.ifirma.pl/iapi/fakturakraj.json"
