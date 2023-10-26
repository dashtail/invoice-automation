import random
import starkbank
from faker import Faker
from app.core.starkbank.auth import get_user
from app.core.starkbank.invoices import Invoice

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