# Invoice Webhook Handler

This project is a FastAPI application that handles webhook events for invoices. It listens for invoice events, processes them, and performs necessary actions based on the event type.

## Features

- Receives and validates webhook events from an external service.
- Handles "invoice credited" events by calculating the total payment and checking if the balance is sufficient.
- Create random invoices every 3 hours
- Check for undelivered events and process them

## Installation

To install the necessary dependencies for this project, you can use pip:

```bash
pip install -r requirements.txt
```

Create a `.env` file:
```
BANK_TAX_ID="12.345.678/0001-10"
BANK_NAME="Bank S.A."
BANK_CODE="0123456"
BANK_BRANCH_CODE="0001"
BANK_ACCOUNT_TYPE="payment"
BANK_ACCOUNT_NUMBER="0099887766"
PROJECT_ENV="sandbox"
PROJECT_ID="098765"
GCP_PROJECT_ID="project-id"
SB_PRIVATE_KEY_NAME="sb_private_key" #GCP Secret Manager
```

Store your private key that will be used in the SDK in GCP Secret Manager

## Usage

To start the server, run:

```
uvicorn main:app --reload
```

The server will start on `http://localhost:8000`.

## Endpoints

`POST /webhook`: Receives a webhook event. The event is expected to be in the format specified by the `WebhookPayload` schema.

## Testing
To run the tests, use:

```
pytest app/tests
```