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
pip install pnowosie-ifirma-api
```

or from this repository
```
pip install +git...
```



