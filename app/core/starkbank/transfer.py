import starkbank
from datetime import datetime
from app.core.starkbank.auth import get_user
from app.core.config import settings


class Transfer:
    def __init__(
        self,
        amount,
        tags=[],
    ):
        self.amount = amount
        self.tax_id = settings.BANK_TAX_ID
        self.name = settings.BANK_NAME
        self.bank_code = settings.BANK_CODE
        self.branch_code = settings.BANK_BRANCH_CODE
        self.account_type = settings.BANK_ACCOUNT_TYPE
        self.account_number = settings.BANK_ACCOUNT_NUMBER
        self.tags = tags

    def create_transfer_object(self):
        transfer = starkbank.Transfer(
            amount=self.amount,
            tax_id=self.tax_id,
            name=self.name,
            bank_code=self.bank_code,
            branch_code=self.branch_code,
            account_type=self.account_type,
            account_number=self.account_number,
            tags=self.tags
        )

        return transfer


def send_transfer(amount, tags=[]):
    user = get_user()
    transfer = starkbank.transfer.create(
        [Transfer(amount=amount, tags=tags).create_transfer_object()],
        user=user,
    )

    return transfer


def calculate_total_payment(invoice):
    return invoice.amount  - invoice.fee
