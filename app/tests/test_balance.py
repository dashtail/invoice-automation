from unittest.mock import Mock, patch
from app.core.starkbank.balance import get_balance

@patch('app.core.starkbank.balance.get_user')
@patch('app.core.starkbank.balance.starkbank.balance.get')
def test_get_balance(mock_get, mock_get_user):
    mock_user = Mock()
    mock_balance = Mock()
    mock_get_user.return_value = mock_user
    mock_get.return_value = mock_balance

    result = get_balance()

    assert result == mock_balance