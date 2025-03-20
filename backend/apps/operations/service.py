from typing import Dict, List, Optional
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from asgiref.sync import sync_to_async

from apps.users.models import User
from apps.operations.models import Operation


class OperationService:
   
    @staticmethod
    @sync_to_async
    def get_operation(operation_id: int) -> Operation:
        try:
            return Operation.objects.prefetch_related("user").get(id=operation_id)
        except Operation.DoesNotExist:
            return None
        
    @staticmethod
    @sync_to_async
    def get_operation_by_payment_id(payment_id: str) -> Operation:
        try:
            return Operation.objects.prefetch_related("user").get(payment_id=payment_id)
        except Operation.DoesNotExist:
            return None
        
    @staticmethod
    @sync_to_async
    def create_operation(
        type: str, method: str, amount: float, user: User, payment_id: Optional[str] = None, wallet: Optional[str] = None
    ) -> Operation:
        return Operation.objects.create(
            type=type, method=method, amount=amount, user=user, payment_id=payment_id, wallet=wallet
        )
    
    @staticmethod
    @sync_to_async
    def update_operation(
        operation_id: int, data: Dict
    ):
        try:
            Operation.objects.filter(id=operation_id).update(**data)
            return True
        except Operation.DoesNotExist:
            return False
        except Exception as e:
            return False
