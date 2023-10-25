import starkbank
from app.core.starkbank.auth import get_user


def get_balance():
    user = get_user()
    balance = starkbank.balance.get(user=user)

    return balance 