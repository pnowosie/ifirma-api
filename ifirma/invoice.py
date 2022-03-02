from datetime import date, timedelta
import ifirma.config as config


class VAT:
    VAT_0 = 0.00
    VAT_5 = 0.05
    VAT_8 = 0.08
    VAT_23 = 0.23


class INVOICE_TYPE:
    VAT_PAYER = 0
    NON_VAT_PAYER = 1


class InvoicePosition:
    def __init__(
        self,
        full_name,
        base_price,
        vat_rate=VAT.VAT_23,
        quantity=1,
        unit="szt",
        flat_rate=None,
    ):
        self.base_price = base_price
        self.full_name = full_name
        self.vat_rate = vat_rate
        self.quantity = quantity
        self.unit = unit
        self.flat_rate = flat_rate


class Customer:
    def __init__(self, full_name, email, zip, city, street1, street2, vat_id=None):
        self.full_name = full_name
        self.email = email
        self.address_abroad = not zip
        self.vat_id = vat_id
        self.zip = zip
        self.city = city
        self.street = (street1 or "") + (f", {street2}" if street2 else "")


class Invoice:
    def __init__(
        self,
        invoice_type=INVOICE_TYPE.VAT_PAYER,
        issue_date=None,
        place=None,
        days=14,
        issuer=None,
    ):
        self.invoice_type = invoice_type
        self.issue_date = issue_date or date.today()
        self.payment_date = self.issue_date + timedelta(days)
        self.issuer = issuer or config.INVOICE_ISSUER
        self.issue_place = place or config.INVOICE_PLACE
        self.positions = []
        self.comments, self.bank_account_no = None, None
        self.payed = 0

    def for_account(self, ban):
        self.bank_account_no = ban
        return self

    def with_position(self, position):
        self.positions.append(position)
        return self

    def with_known_customer(self, identifier, tax_id, eu_prefix="PL"):
        self.known_customer = dict(id=identifier, tax_id=tax_id, prefix=eu_prefix)
        return self

    def with_comments(self, comments):
        self.comments = comments
        return self

    def with_issuer(self, issuer):
        self.issuer = issuer
        return self

    def with_payed(self, amount):
        self.payed = amount
        return self

    def with_new_customer(self, customer):
        self.new_customer = customer
        return self
