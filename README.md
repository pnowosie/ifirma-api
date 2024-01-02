# Python wrapper for [ifirma's API](https://api.ifirma.pl)

Requires `Python 3.8` or later.
This little project aims to refresh my python coding skills.

Besides coding fun this code also supported invoicing in a few small online shops. It does its job pretty well.

First version was inspired of @DariuszAniszewski's [python-ifirma](https://github.com/DariuszAniszewski/python-ifirma)
but covers slightly different operations and has evolved over the years to support more use cases.

Natively supported by this package invoice type is ifirma's `faktura krajowa`.
However is not that hard to create other invoice types using arbitrary request feature.
Which is just to send any ifirma's json request from file template, you can find examples in `sample_invoice` folder.

## Features

It supports following operations

- create invoice (VAT & non-VAT payers)
- [listing invoices created in past](/sample_invoice/list_invoices.py)
- [send email with pdf-invoice attached](/sample_invoice/main.py) (it sends also copy to the account owner)
- [download invoice in pdf format](/sample_invoice/main.py)
- allows to authenticate and [send arbitrary json request](/sample_invoice/send_arbitrary_requests.py)
- invoice can be described with [yaml format](/sample_invoice/consensius.yml)

## When you add more? Are PRs welcomed?

Probably never. It's here to support my business.
If you're looking for ideas how to extend it, 👉 see arbitrary requests from `sample_invoice` directory.
These might be mostly interested if some non-standard ifirma's api operation is required:

- [Arbitrary request of other type of invoice](/sample_invoice/send_arbitrary_other_requests.py)
- [Check and change the current accounting month](/sample_invoice/check_accounting_month.py)

Other ideas of extension can be find in [issue #8](https://github.com/pnowosie/ifirma-api/issues/8) discusion.

## Getting started

Finally ifirma-api got a proper python packaging process :) and newest version can
be installed from PyPI.

```
pip install pnowosie.ifirma-api=={VERSION}
```

or directly from GitHub from this repository, commit's id (SHA) and can be ommitted (defaults to HEAD).

```
pip install -e git+https://github.com/pnowosie/ifirma-api.git@{SHA}#egg=pnowosie.ifirma-api
```


## Invoice creation

Please review examples in `./sample_invoice` directory. You will find there how to create invoice from yaml file.
Send it via email and download pdf version to a location of choice.

Or create invoice from code

```python
from ifirma.invoice import (Invoice, Customer, InvoicePosition, INVOICE_TYPE)

invoice = Invoice(
    invoice_type=INVOICE_TYPE.NON_VAT_PAYER,
    issue_date=datetime(...)
).with_issuer(
    'Imię Nazwisko'
).with_payed(
    float(price)
).with_comments(
    f"Nr zamówienia: {numer}"
).with_position(
    InvoicePosition(product_name, float(price), flat_rate=float(ryczałt))
).with_new_customer(
    Customer(full_name, email, zip, city, street1, street2)
)
```

if you registered your customer in `ifirma` you can use

```python
invoice.with_known_customer(
  name, tax_id
)
```

Having invoice object, we can send it to create an invoice in the ifirma. Please mind that two environment variables
IFIRMA_API_USERNAME and IFIRMA_API_KEY have to be set to authenticate API request.

```python
from ifirma import api

create_invoice_response = api.create_invoice(invoice)

if create_invoice_response.success:
    print(f"Invoice created with id {create_invoice_response}")
else:
    print("Something bad has happened: " + create_invoice_response.message)
```

Next step can be send an email with the invoice attached to the customer email address. CC is delivered also to our
address registered in the ifirma.

```python
from ifirma import api

custom_message = "Can you please send me more money? I'm getting ambitious vacation plans!"
email_send_response = api.email_invoice(invoice_id, customer_email_address, custom_message)
```

If the pdf copy of the invoice is needed to be stored, we can download it as well

```python
from ifirma import api
from pathlib import Path

file_path = Path('/tmp') / f"invoice_{invoice_id}.pdf"
api.download_invoice(invoice_id, file_path)
```

Please check [this example](https://github.com/pnowosie/ifirma-api/blob/main/sample_invoice/main.py).

## Special Thanks

- @DariuszAniszewski - [his project](https://github.com/DariuszAniszewski/python-ifirma) was an inspiration,
- @krystianmagdziarz - who helped and contribute to examples,
- @daneah for his amaizing book "Publishing Python Packages" which finally taugh me packaging mastery (or monkey-ry, choose most fitting)
