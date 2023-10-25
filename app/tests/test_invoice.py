import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.core.starkbank.transfer import calculate_total_payment

client = TestClient(app)

class TestInvoiceEndpoint(unittest.TestCase):
    def setUp(self):
        self.event = MagicMock()
        self.event.subscription = "invoice"
        self.event.log.type = "credited"
        self.event.log.invoice = MagicMock()
        self.event.log.invoice.id = "1"
        self.event.dict.return_value = {
            "id": "01234",
            "subscription": self.event.subscription,
            "log": {
                "id": "0987",
                "type": self.event.log.type,
                "invoice": {
                    "id": self.event.log.invoice.id,
                    "amount": 0,
                    "fee": 0,
                    "fine": 0,
                    "interest": 0,
                    "due": "2021-01-01T00:00:00",
                    "discounts": [],
                }
            }
        }

    @patch("app.api.endpoints.invoice.get_balance")
    @patch("app.api.endpoints.invoice.send_transfer")
    def test_webhook_transfer_successful(self, mock_send_transfer, mock_get_balance):
        mock_get_balance.return_value = 1000
        self.event.log.invoice.amount = 1000
        self.event.log.invoice.fee = 50
        self.event.log.invoice.fine = 2
        self.event.log.invoice.interest = 1
        self.event.log.invoice.due = "2022-01-01T00:00:00"
        self.event.log.invoice.discounts = [
            {'percentage': 10, 'due': '2022-01-05T00:00:00'},
        ]
        calculate_total_payment.return_value = 750
        response = client.post("/api/invoice/webhook", json=self.event.dict())
        assert response.status_code == 200
        assert response.json() == {"message": "Transfer successful"}
        

    @patch("app.api.endpoints.invoice.get_balance")
    def test_webhook_transfer_failed(self, mock_get_balance):
        mock_get_balance.return_value = 1000
        self.event.log.invoice.amount = 1000
        self.event.log.invoice.fee = 50
        self.event.log.invoice.fine = 2
        self.event.log.invoice.interest = 1
        self.event.log.invoice.due = "2022-01-01T00:00:00"
        self.event.log.invoice.discounts = [
            {'percentage': 10, 'due': '2022-01-05T00:00:00'},
        ]
        calculate_total_payment.return_value = 750
        with patch("app.api.endpoints.invoice.send_transfer", side_effect=Exception):
            response = client.post("/api/invoice/webhook", json=self.event.dict())
            assert response.status_code == 200
            assert response.json() == {"message": "Transfer failed"}

    @patch("app.api.endpoints.invoice.get_balance")
    def test_webhook_insufficient_balance(self, mock_get_balance):
        mock_get_balance.return_value = 500
        self.event.log.invoice.amount = 1000
        response = client.post("/api/invoice/webhook", json=self.event.dict())
        assert response.status_code == 200
        assert response.json() is None
