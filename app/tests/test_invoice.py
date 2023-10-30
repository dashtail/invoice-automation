import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.core.starkbank.transfer import calculate_total_payment
from app.schemas.webhook import InvoiceDetailSchema
from datetime import datetime

client = TestClient(app)


class TestInvoiceEndpoint(unittest.TestCase):
    def setUp(self):
        
        self.event = MagicMock()
        self.event.subscription = "invoice"
        self.event.log.type = "credited"
        self.invoice_id = "1"
        self.invoice_amount = 1000
        self.invoice_fee = 0
        self.invoice_fine = 0
        self.event.dict.return_value = {
            "event": {
                "id": "01234",
                "subscription": self.event.subscription,
                "log": {
                    "id": "0987",
                    "type": self.event.log.type,
                    "invoice": {
                        "id": self.invoice_id,
                        "amount": self.invoice_amount,
                        "fee": self.invoice_fee,
                        "fine": self.invoice_fine,
                        "interest": 0,
                        "due": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                        "discounts": [],
                        "expiration": 5097600.0,
                        "name": "test name",
                        "rules": [],
                        "tags": [],
                        "pdf": "pdf_url",
                        "link": "link_url",
                        "descriptions": [],
                        "brcode": "brcode",
                        "status": "paid",
                        "created": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                        "updated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                    },
                },
            }
        }

    @patch("starkbank.balance.get")
    @patch("app.api.endpoints.invoice.send_transfer")
    @patch("starkbank.event.parse")
    def test_webhook_transfer_successful(
        self, mock_starkbank_event_parse, mock_send_transfer, mock_get_balance, 
    ):
        mock_get_balance.return_value = MagicMock(amount=20000)
        mock_send_transfer.return_value = True
        mock_starkbank_event_parse.return_value = True
    
        calculate_total_payment.return_value = 750
        headers = {"Digital-Signature": "signature"}
        response = client.post(
            "/api/invoice/webhook", json=self.event.dict(), headers=headers
        )
        print(response.json())
        assert response.status_code == 200
        assert response.json() == {"message": "Transfer successful"}

    @patch("starkbank.balance.get")
    @patch("starkbank.event.parse")
    def test_webhook_transfer_failed(
        self, mock_starkbank_event_parse, mock_get_balance
    ):
        mock_starkbank_event_parse.return_value = True
        mock_get_balance.return_value = MagicMock(amount=5000)
        calculate_total_payment.return_value = 750
        
        with patch("starkbank.transfer.create", side_effect=Exception):
            headers = {"Digital-Signature": "signature"}
            response = client.post(
                "/api/invoice/webhook", json=self.event.dict(), headers=headers
            )
            print(response)
            assert response.status_code == 500

    @patch("starkbank.balance.get")
    @patch("starkbank.event.parse")
    def test_webhook_insufficient_balance(
        self, mock_starkbank_event_parse, mock_get_balance 
    ):
        mock_starkbank_event_parse.return_value = True
        mock_get_balance.return_value = MagicMock(amount=300)
        headers = {"Digital-Signature": "signature"}
        response = client.post(
            "/api/invoice/webhook", json=self.event.dict(), headers=headers
        )
        assert response.status_code == 400
        assert response.json() == {'detail': 'No balance available'}
