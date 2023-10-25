from pydantic import BaseModel


class InvoiceDetailSchema(BaseModel):
    id: str
    amount: int
    fine_amount: int
    interest_amount: int
    discount_amount: int
    due: str
    tax_id: str
    name: str
    expiration: float
    fine: float
    interest: float
    discounts: list
    rules: list
    tags: list
    pdf: str
    link: str
    descriptions: list
    brcode: str
    status: str
    fee: int
    transaction_ids: list
    created: str
    updated: str


class LogSchema(BaseModel):
    id: str
    type: str
    invoice: InvoiceDetailSchema


class WebhookEvent(BaseModel):
    id: str
    subscription: str
    log: LogSchema

