from pydantic import BaseModel


class InvoiceDetailSchema(BaseModel):
    id: str
    amount: int
    fine_amount: int = None
    interest_amount: int = None
    discount_amount: int = None
    due: str
    tax_id: str = None
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
    transaction_ids: list = None
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


class WebhookPayload(BaseModel):
    event: WebhookEvent

