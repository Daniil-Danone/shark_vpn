from typing import Dict, List, Optional, Tuple
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
            return Receipt.objects.prefetch_related("tariff", "user").get(id=receipt_id)
        except Receipt.DoesNotExist:
            return None
        
    @staticmethod
    @sync_to_async
    def get_receipt_by_payment_id(payment_id: str) -> Receipt:
        try:
            return Receipt.objects.prefetch_related("tariff", "user").get(payment_id=payment_id)
        except Receipt.DoesNotExist:
            return None

    @staticmethod
    @sync_to_async
    def create_receipt(user: User, tariff: Tariff, payment_id: Optional[str] = None) -> Receipt:
        return Receipt.objects.create(user=user, tariff=tariff, payment_id=payment_id)
    
    @staticmethod
    @sync_to_async
    def update_receipt(receipt_id: int, data: Dict) -> bool:
        try:
            Receipt.objects.filter(id=receipt_id).update(**data)
            return True
        except Receipt.DoesNotExist:
            return False
        except Exception as e:
            return False
    
    @staticmethod
    @sync_to_async
    def set_message_id(receipt_id: int, message_id: int) -> bool:
        try:
            Receipt.objects.filter(id=receipt_id).update(message_id=message_id)
            return True
        except Receipt.DoesNotExist:
            return False
        except Exception as e:
            return False