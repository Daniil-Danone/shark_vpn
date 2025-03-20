import json
import uuid
import logging
import requests
from typing import Dict, Optional, Tuple
from requests.auth import HTTPBasicAuth

from config.environment import (
    CLIENT_ID, CLIENT_SECRET, REDIRECT_URL,
    INIT_PAYMENT_URL, CHECK_PAYMENT_STATUS_URL, CANCEL_PAYMENT_URL, 
    SUCCEEDED, CANCELED
)


def init_payment(amount: float, description: str, client_fullname: str, client_email: str) -> Tuple[str, str]:
    payload = {
        "amount": { 
            "value": f"{amount:.2f}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect", 
            "return_url": REDIRECT_URL
        },
        "receipt": {
            "customer": {
                "full_name": client_fullname,
                "email": client_email
            },
            "items": [
                {
                    "description": description,
                    "amount": {
                        "value": f"{amount:.2f}",
                        "currency": "RUB"
                    },
                    "vat_code": 1,
                    "quantity": 1,
                    "payment_subject": "commodity",
                    "payment_mode": "full_payment"
                }
            ]
        },
        "capture": True,
        "description": description,
        "save_payment_method": True
    }

    headers = {
        "Idempotence-Key": str(uuid.uuid4()),
        "Content-Type": "application/json"
    }

    response = requests.post(
        url=INIT_PAYMENT_URL,
        json=payload,
        headers=headers,
        auth=HTTPBasicAuth(
            username=CLIENT_ID, 
            password=CLIENT_SECRET
        )
    )

    if response.status_code != 200:
        raise RuntimeError(f"[INIT] Failed to init payment: {response.text}")
    
    data: Dict[str, Dict[str, str]] = json.loads(response.text)

    payment_id = data.get("id")
    payment_url = data.get("confirmation").get("confirmation_url")

    logging.info(f"[INIT] Payment init successfully.")

    return payment_id, payment_url


def check_status(payment_id: str) -> Tuple[bool, Optional[str]]:
    response = requests.get(
        url=CHECK_PAYMENT_STATUS_URL.format(payment_id=payment_id),
        auth=HTTPBasicAuth(
            username=CLIENT_ID,
            password=CLIENT_SECRET
        )
    )

    if response.status_code != 200:
        raise RuntimeError(f"[STATUS] Failed to check payment status: {response.text}")
    
    data: Dict[str, str] = json.loads(response.text)

    status = data.get("status")
    if status != SUCCEEDED:
        logging.info(f"[STATUS] Payment is not confirmed yet. Current status: {status}")
        return False
    
    payment_method_id = None
    payment_method: Optional[Dict[str, str]] = data.get("payment_method", None)
    if payment_method:
        payment_method_id: str = payment_method.get("id")
    
    logging.info(f"[STATUS] Payment confirmed successfully.")
    return True, payment_method_id


def init_recurrent_payment(amount: float, payment_method_id: str, description: str) -> str:
    payload = {
        "amount": {
            "value": f"{amount:.2f}",
            "currency": "RUB"
        },
        "capture": True,
        "payment_method_id": payment_method_id,
        "description": description
    }

    headers = {
        "Idempotence-Key": str(uuid.uuid4()),
        "Content-Type": "application/json"
    }

    response = requests.post(
        url=INIT_PAYMENT_URL,
        json=payload,
        headers=headers,
        auth=HTTPBasicAuth(
            username=CLIENT_ID, 
            password=CLIENT_SECRET
        )
    )

    if response.status_code != 200:
        raise RuntimeError(f"[INIT] Failed to init recurrent payment: {response.text}")
    
    data: Dict[str, Dict[str, str]] = json.loads(response.text)

    payment_id = data.get("id")

    logging.info(f"[INIT] Recurrent payment init successfully.")

    return payment_id

def cancel_payment(payment_id: str):
    headers = {
        "Idempotence-Key": str(uuid.uuid4()),
        "Content-Type": "application/json"
    }

    response = requests.post(
        url=CANCEL_PAYMENT_URL.format(payment_id=payment_id),
        auth=HTTPBasicAuth(
            username=CLIENT_ID,
            password=CLIENT_SECRET
        ),
        headers=headers,
        json={}
    )

    if response.status_code != 200:
        raise RuntimeError(f"[CANCEL] Failed to cancel payment: {response.text}")
    
    data: Dict[str, str] = json.loads(response.text)

    status = data.get("status")
    if status != CANCELED:
        logging.info(f"[CANCEL] Payment is not canceled yet. Current status: {status}")
        return False
    
    logging.info(f"[STATUS] Payment canceled successfully.")
    return True