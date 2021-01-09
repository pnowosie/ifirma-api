# Python wrapper for [ifirma's API](https://api.ifirma.pl)

Requires `Python 3.8` or later. 
This little project aims to refresh my python coding skills.

Besides coding fun this code also supported invoicing in a few small online shops. It does its job pretty well.

First version was inspired of @DariuszAniszewski's [python-ifirma](https://github.com/DariuszAniszewski/python-ifirma) but covers slightly different operations.

## Features

It supports following operations
- create invoice (VAT payer)
- create invoice (non-VAT payer)
- send email with pdf-invoice attached (it sends also copy to the account owner)
- parses invoice described with yaml file

## Getting started

```
pip install pnowosie.ifirma-api
```

or from this repository
```
pip install -e git+git@github.com:pnowosie/ifirma-api.git#egg=pnowosie.ifirma-api
```
## Invoice creation

Please review example from `./sample_invoice` directory. You will find there how to create and send invoice via email with yaml file.

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
    InvoicePosition(product_name, float(price)
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
