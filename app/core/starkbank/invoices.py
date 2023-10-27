import starkbank
from datetime import datetime, timedelta

class Invoice:
    def __init__(
        self,
        amount,
        name,
        tax_id,
    ):
        self.amount = amount
        self.name = name
        self.tax_id = tax_id

    def create_invoice_object(self):
        invoice = starkbank.Invoice(
            amount=self.amount,
            name=self.name,
            tax_id=self.tax_id,
        )

        return invoice


