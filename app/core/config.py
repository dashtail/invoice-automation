import os
from dotenv import load_dotenv
from google.cloud import secretmanager

load_dotenv()


class Settings:
    BANK_TAX_ID: str = os.getenv("BANK_TAX_ID")
    BANK_NAME: str = os.getenv("BANK_NAME")
    BANK_CODE: str = os.getenv("BANK_CODE")
    BANK_BRANCH_CODE: str = os.getenv("BANK_BRANCH_CODE")
    BANK_ACCOUNT_TYPE: str = os.getenv("BANK_ACCOUNT_TYPE")
    BANK_ACCOUNT_NUMBER: str = os.getenv("BANK_ACCOUNT_NUMBER")
    PROJECT_ID: str = os.getenv("PROJECT_ID")
    PROJECT_ENV: str = os.getenv("PROJECT_ENV")
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID")
    SB_PRIVATE_KEY_NAME: str = os.getenv("SB_PRIVATE_KEY_NAME")

    @property
    def starkbank_private_key(self):
        client = secretmanager.SecretManagerServiceClient()
        response = client.access_secret_version(
            name=f"projects/{self.GCP_PROJECT_ID}/secrets/{self.SB_PRIVATE_KEY_NAME}/versions/latest"
        )
        secret_payload = response.payload.data.decode("UTF-8")

        return secret_payload

    class Config:
        case_sensitive = True


settings = Settings()
