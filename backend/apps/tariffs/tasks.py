from typing import Dict
from config.celery_app import app
from asgiref.sync import async_to_sync

from bot.services import payment


@app.task
def send_payment_success(payment_id: str, payment_object: Dict):
    async_to_sync(payment.send_confirm)(payment_id=payment_id, payment_object=payment_object)


@app.task
def send_payment_cancel(payment_id: str):
    async_to_sync(payment.send_cancel)(payment_id=payment_id)