from ifirma.yaml_parser import parse
from ifirma.invoice import Invoice

INVOICE_YAML = """
issue_place: Krychnowice
issuer: Jan Nowak

known_customer:
  name: Klient Widmo
  tax_id: '0000000000'

positions:
  - name: Pozycja, której nie umiem wyjaśnić
    amount: 1.23
  - name: Kolejna drozsza od 👆 o tej
    amount: 9.99

ban: '00000000000000000000000000000000'
comments: >
  Fakturę tę komentuję ją
"""

SEND_EMAIL_YAML = """

send_to: email@example.com
"""


def test_parser_returns_invoice():
    task = parse(INVOICE_YAML)
    assert 'invoice' in task.keys()
    assert isinstance(task['invoice'], Invoice)

def test_parser_parses_customer():
    task = parse(INVOICE_YAML)
    invoice = task['invoice']
    assert {'id': 'Klient Widmo', 'tax_id': '0000000000', 'prefix': 'PL'} == invoice.known_customer

def test_parser_parses_positions_smoke():
    task = parse(INVOICE_YAML)
    invoice = task['invoice']
    assert 2 == len(invoice.positions)

def test_parser_parses_positions():
    task = parse(INVOICE_YAML)
    invoice = task['invoice']
    [_p1, p2] = invoice.positions

    assert p2.full_name == 'Kolejna drozsza od 👆 o tej'
    assert p2.base_price == 9.99
    assert p2.unit == 'szt'
    assert p2.quantity == 1

def test_parser_parses_ban():
    task = parse(INVOICE_YAML)
    invoice = task['invoice']
    assert '00000000000000000000000000000000' == invoice.bank_account_no

def test_parser_parses_comment():
    task = parse(INVOICE_YAML)
    invoice = task['invoice']
    assert 'Fakturę tę komentuję ją' == invoice.comments

def test_parser_parses_issue_place():
    task = parse(INVOICE_YAML)
    invoice = task['invoice']
    assert 'Krychnowice' == invoice.issue_place

def test_parser_parses_issuer():
    task = parse(INVOICE_YAML)
    invoice = task['invoice']
    assert 'Jan Nowak' == invoice.issuer

def test_invoice_has_todays_issue_date():
    from datetime import date
    task = parse(INVOICE_YAML)
    invoice = task['invoice']
    assert date.today() == invoice.issue_date

def test_invoice_has_default_payment_date():
    from datetime import date, timedelta
    pay_date = date.today() + timedelta(14)
    task = parse(INVOICE_YAML)
    invoice = task['invoice']
    assert pay_date == invoice.payment_date

def test_sending_invoice_by_email():
    task = parse(INVOICE_YAML+SEND_EMAIL_YAML)
    email = task['send_to']
    assert email == 'email@example.com'

def test_simple_invoice_without_ban_and_comments():
    simple_invoice = """
known_customer:
  name: Klient Widmo
  tax_id: '0000000000'
positions:
  - name: Waciki
    amount: 100.00
"""

    task = parse(simple_invoice)
    invoice = task['invoice']
    assert None == invoice.bank_account_no
    assert None == invoice.comments

def test_simple_invoice_with_issue_date():
    from datetime import date
    simple_invoice = """
issue_date: 2020-06-19
known_customer:
  name: Klient Widmo
  tax_id: '0000000000'
positions:
  - name: Waciki
    amount: 100.00
"""

    task = parse(simple_invoice)
    invoice = task['invoice']
    assert date(2020, 6, 19) == invoice.issue_date
