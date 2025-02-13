from typing import List, Optional, Tuple
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from asgiref.sync import sync_to_async

from apps.tariffs.models import Tariff, Receipt
from apps.users.models import User


class TariffService:
    @staticmethod
    @sync_to_async
    def get_tariffs() -> List[Tariff]:
        tariffs = Tariff.objects.filter(is_active=True)
        return list(tariffs)
    
    @staticmethod
    @sync_to_async
    def get_tariff(tariff_id: int) -> Tariff:
        try:
            return Tariff.objects.get(id=tariff_id)
        except Tariff.DoesNotExist:
            return None
    

class ReceiptService:

    @staticmethod
    @sync_to_async
    def get_receipt(receipt_id: int) -> Receipt:
        try:
            return Receipt.objects.prefetch_related("tariff").get(id=receipt_id)
        except Receipt.DoesNotExist:
            return None

    @staticmethod
    @sync_to_async
    def create_receipt(user: User, tariff: Tariff, payment_id: Optional[str] = None) -> Receipt:
        return Receipt.objects.create(user=user, tariff=tariff, payment_id=payment_id)
    
    @staticmethod
    @sync_to_async
    def update_receipt(receipt_id: int, payment_status: str) -> Receipt:
        receipt = Receipt.objects.get(id=receipt_id)
        if not receipt:
            return
        
        if payment_status in ["done", "balance"]:
            now = timezone.now()
            
            receipt.status = payment_status
            receipt.payed_at = now
            
        elif payment_status == "cancel":
            receipt.status = payment_status

        receipt.save()

        return receipt