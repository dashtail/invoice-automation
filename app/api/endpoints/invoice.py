from fastapi import APIRouter, HTTPException
from app.core.starkbank.transfer import send_transfer
from app.schemas.webhook import WebhookPayload
from app.core.starkbank.transfer import calculate_total_payment
from app.core.starkbank.balance import get_balance

router = APIRouter()


@router.post("/webhook")
def webhook(payload: WebhookPayload):
    event = payload.event
    if event.subscription == "invoice":
        if event.log.type == "credited":
            balance = get_balance()
            amount = calculate_total_payment(event.log.invoice)
            if balance.amount > amount:
                try:
                    send_transfer(
                        amount,
                        tags=[f"invoice #{event.log.invoice.id}", f"event #{event.id}"],
                    )
                    return {"message": "Transfer successful"}
                except Exception as e:
                    raise HTTPException(status_code=500, detail=e)
            else:
                raise HTTPException(status_code=400, detail="No balance available")

    return {"message": "No transfer needed"}
