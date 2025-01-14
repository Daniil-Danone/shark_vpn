from typing import List, Optional
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
            return Operation.objects.get(id=operation_id)
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
        operation_id: int, status: str
    ) -> Operation:
        operation = Operation.objects.get(id=operation_id)
        if not operation:
            return None
        
        now = timezone.now()

        operation.status = status
        
        if status == "done":
            operation.completed_at = now
            
        elif status == "cancel":
            operation.cancelled_at = now

        operation.save()
        return operation
