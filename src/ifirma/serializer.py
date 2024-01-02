from ifirma.invoice import INVOICE_TYPE, Invoice, InvoicePosition


def _format_date(date):
    return "{t.year}-{t.month:0>2d}-{t.day:0>2d}".format(t=date)


def _make_invoice_generic_position(position):
    assert isinstance(
        position, InvoicePosition
    ), f"Expected ifirma.InvoicePosition type but got {type(position)}"

    pos = {
        "Ilosc": position.quantity,
        "CenaJednostkowa": position.base_price,
        "NazwaPelna": position.full_name,
        "Jednostka": position.unit,
    }

    # add optional fields
    if position.flat_rate:
        pos["StawkaRyczaltu"] = position.flat_rate

    return pos


def _make_invoice_position_vat(position):
    return {
        **_make_invoice_generic_position(position),
        "StawkaVat": position.vat_rate,
        "PKWiU": "",
        "TypStawkiVat": "PRC",
    }


def _make_invoice_position_non_vat(position):
    return {
        **_make_invoice_generic_position(position),
        "PodstawaPrawna": "Art. 113 ust. 1",
        "StawkaVat": None,
        "TypStawkiVat": "ZW",
    }


def _invoice_new_customer(customer):
    part = {
        "Nazwa": customer.full_name,
        "Identyfikator": None,
        "Email": customer.email,
        "OsobaFizyczna": True,
        "AdresZagraniczny": customer.address_abroad,
    }

    if customer.vat_id:
        part["OsobaFizyczna"] = False
        part["NIP"] = customer.vat_id

    if not customer.address_abroad:
        part.update(
            {
                "KodPocztowy": customer.zip,
                "Miejscowosc": customer.city,
                "Ulica": customer.street,
            }
        )

    return part


def make_customer_part(invoice):
    if known_customer := getattr(invoice, "known_customer", None):
        return {
            "IdentyfikatorKontrahenta": known_customer["id"],
            "PrefiksUEKontrahenta": known_customer["prefix"],
            "NIPKontrahenta": known_customer["tax_id"],
        }
    elif new_customer := getattr(invoice, "new_customer", None):
        return {"Kontrahent": _invoice_new_customer(new_customer)}


def include_optional(idict, optionals):
    for key, value in optionals:
        if value:
            idict[key] = value


def make_invoice_position_for(invoice):
    return {
        INVOICE_TYPE.VAT_PAYER: _make_invoice_position_vat,
        INVOICE_TYPE.NON_VAT_PAYER: _make_invoice_position_non_vat,
    }[invoice.invoice_type]


_invoice_sane_defaults = {
    INVOICE_TYPE.VAT_PAYER: {
        "LiczOd": "NET",
        "SplitPayment": False,
        "SposobZaplaty": "PRZ",
    },
    INVOICE_TYPE.NON_VAT_PAYER: {
        "LiczOd": "BRT",
        "SposobZaplaty": "ELE",
    },
}


def make_invoice(invoice):
    assert isinstance(
        invoice, Invoice
    ), f"Expected ifirma.Invoice type but got {type(invoice)}"

    position_creator = make_invoice_position_for(invoice)
    idict = _invoice_sane_defaults[invoice.invoice_type].copy()
    idict.update(
        {
            "DataWystawienia": _format_date(invoice.issue_date),
            "DataSprzedazy": _format_date(invoice.issue_date),
            "FormatDatySprzedazy": "DZN",
            "TerminPlatnosci": _format_date(invoice.payment_date),
            "RodzajPodpisuOdbiorcy": "BPO",
            "NazwaSzablonu": "Logo",
            "WidocznyNumerGios": False,
            "Numer": None,
            "Pozycje": list(map(position_creator, invoice.positions)),
            "Zaplacono": invoice.payed,
        }
    )

    customer_part = make_customer_part(invoice)
    idict.update(customer_part)

    include_optional(
        idict,
        [
            ("MiejsceWystawienia", invoice.issue_place),
            ("NumerKontaBankowego", invoice.bank_account_no),
            ("PodpisWystawcy", invoice.issuer),
            ("Uwagi", invoice.comments),
            ("ZaplaconoNaDokumencie", invoice.payed),
        ],
    )

    return idict


def make_email(
    to_address,
    text="W załączeniu przesyłam fakturę dotyczącą zamówienia",
    from_address="faktury@ifirma.pl",
    template="Domyślny ifirma.pl",
):
    return {
        "Tekst": text,
        "SkrzynkaEmail": from_address,
        "SzablonEmail": template,
        "SkrzynkaEmailOdbiorcy": to_address,
    }
