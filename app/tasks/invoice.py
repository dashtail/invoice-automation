import random
import starkbank
from faker import Faker
from datetime import datetime, timedelta
from app.core.starkbank.auth import get_user
from app.core.starkbank.balance import get_balance
from app.core.starkbank.invoices import Invoice
from app.core.starkbank.transfer import send_transfer, calculate_total_payment

def create_invoices():
    invoices = []
    fake = Faker("pt_BR")
    number_of_invoices = random.randint(8, 12)
    user = get_user()

    try:
        for _ in range(number_of_invoices):
            invoice = Invoice(
                amount=random.randint(5000, 250000),
                name=fake.name(),
                tax_id=fake.cpf(),
            ).create_invoice_object()

            invoices.append(invoice)
            
        invoices = starkbank.invoice.create(invoices, user=user)
        
        print("Invoices created successfully")

    except Exception as e:
        print(e)
        return None

    return invoices

def get_undelivered_events():
    user = get_user()
    before_date = datetime.now()
    after_date = before_date - timedelta(days=2)
 
    events = starkbank.event.query(
        is_delivered=False,
        after=after_date.strftime("%Y-%m-%d"),
        before=before_date.strftime("%Y-%m-%d"),
        user=user,
    )
 
    for event in events:
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
                    print(f"log --->: {e}")
            else:
                print(
                    "No balance available",
                    f"invoice #{event.log.invoice.id} event #{event.id}",
                )
 
        starkbank.event.update(event.id, is_delivered=True, user=user)
 
    return