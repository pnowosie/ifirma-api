# Python wrapper for [ifirma's API](https://api.ifirma.pl)

Requires `Python 3.8` or later. 
This little project aims to refresh my python coding skills.

Besides coding fun this code also supported invoicing in a few small online shops. It does its job pretty well.

First version was inspired of @DariuszAniszewski's [python-ifirma](https://github.com/DariuszAniszewski/python-ifirma) 
but covers slightly different operations.

## Features

It supports following operations
- create invoice (VAT & non-VAT payers)
- [listing invoices created in past](/sample_invoice/list_invoices.py)
- send email with pdf-invoice attached (it sends also copy to the account owner)
- parses invoice described with yaml file
- download invoice in pdf format

## When you add more? Are PRs welcomed?

Probably never. It's here to support my business. 
If you're looking for ideas how to extend it, 👉 see [issue #8](https://github.com/pnowosie/ifirma-api/issues/8)

## Getting started

```
pip install pnowosie.ifirma-api
```

or from this repository
```
pip install -e git+git@github.com:pnowosie/ifirma-api.git#egg=pnowosie.ifirma-api
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
    InvoicePosition(product_name, float(price))
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
import ifirma.api as Api

create_invoice_response = Api.create_invoice(invoice)

if create_invoice_response.success:
    print(f"Invoice created with id {create_invoice_response}")
else:
    print("Something bad has happened: " + create_invoice_response.message)
```

Next step can be send an email with the invoice attached to the customer email address. CC is delivered also to our
address registered in the ifirma.

```python
import ifirma.api as Api

custom_message = "Can you please send me more money? I'm getting ambitious vacation plans!"
email_send_response = Api.email_invoice(invoice_id, customer_email_address, custom_message)
```

If the pdf copy of the invoice is needed to be stored, we can download it as well

```python
import ifirma.api as Api
from pathlib import Path

file_path = Path('/tmp') / f"invoice_{invoice_id}.pdf"
Api.download_invoice(invoice_id, file_path)
```

Please check [this example](https://github.com/pnowosie/ifirma-api/blob/main/sample_invoice/main.py).
