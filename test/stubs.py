from datetime import date
from ifirma.invoice import Invoice, InvoicePosition, Customer
from ifirma.serializer import make_email
from ifirma.config import configure

configure(place='Warszawa', issuer='Paweł Nowosielski')

SAMPLE_API_USER='jan.nowak@ifirma.pl'

_invoice = lambda: Invoice(issue_date=date(2020, 7, 23)
   ).with_comments('Komentarz swój pozostawiam'
   ).with_position(
      InvoicePosition(
         'Pozycja której nie umiem wyjaśnić', 1.23)
   ).with_position(
      InvoicePosition(
         'Kolejna droższa od 👆o tej', 9.99)
   )

INVOICE_WITH_KNOWN_CUSTOMER = _invoice().for_account(
      '00000000000000000000000000'
   ).with_known_customer(
      'Klient WIDMO', '0000000000'
   )

PAYED_INVOICE_WITH_NEW_CUSTOMER = _invoice().with_payed(
      11.22
   ).with_new_customer(
      Customer('Jan Nowak', 'jan@nowak.pl', '00-000', 'Warszawa', 'Al. Jerozolimskie', '111/22')
   )

PAYED_NONVAT_INVOICE_FOR_COMPANY = _invoice().with_payed(
      11.22
   ).with_new_customer(
      Customer('EDOPI Software', 'kontakt@edopi.pl', '00-000', 'Warszawa', 'Al. Jerozolimskie', '111/22',
         vat_id='PL1234567890')
   )

SEND_EMAIL_WITH_INVOICE_REQUEST = make_email(SAMPLE_API_USER, 'W zalaczeniu przesylam fakturke\n\nUszanowania,\nJan Nowak')
