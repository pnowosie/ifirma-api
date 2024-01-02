from datetime import date

from yaml import load, FullLoader

from ifirma.invoice import Invoice, InvoicePosition

today = date.today()
DEFAULT_EMAIL_MESSAGE = (
    f"W załączeniu przesyłam fakturę za {today.year}/{today.month:02}.\nPozdrawiam :)"
)


def parse(str):
    doc = load(str, Loader=FullLoader)

    invoice = Invoice(
        issue_date=doc.get("issue_date"),
        issuer=doc.get("issuer"),
        place=doc.get("issue_place"),
    ).with_known_customer(
        doc["known_customer"]["name"], doc["known_customer"]["tax_id"]
    )

    if doc.get("ban"):
        invoice.bank_account_no = doc["ban"]
    if doc.get("comments"):
        invoice.comments = doc["comments"].strip()

    invoice.positions = list(
        map(
            lambda pos: InvoicePosition(
                pos["name"], pos["amount"], flat_rate=pos.get("flat_rate")
            ),
            doc["positions"],
        )
    )
    task = dict(invoice=invoice)

    if doc.get("send_to"):
        task["send_to"] = doc["send_to"]
        task["message"] = doc.get("message") or DEFAULT_EMAIL_MESSAGE

    if doc.get("download"):
        task["download"] = doc["download"]

    return task
