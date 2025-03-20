from typing import List, Optional
from asgiref.sync import sync_to_async

from apps.users.models import User
from apps.referals.models import Referal


class ReferalService:
    @staticmethod
    @sync_to_async
    def get_referals(partner_id: int) -> List[Referal]:
        referals = Referal.objects.prefetch_related(
            "partner", "referal"
        ).filter(partner__user_id=partner_id)
        return list(referals)
    
    @staticmethod
    @sync_to_async
    def get_referal(partner_id: int, referal_id: int) -> Referal:
        try:
            return Referal.objects.get(
                partner__user_id=partner_id, referal__user_id=referal_id
            )
        except Referal.DoesNotExist:
            return None
    
    @staticmethod
    @sync_to_async
    def get_partner_by_referal(referal_id: int) -> User:
        try:
            referal = Referal.objects.get(
                referal__user_id=referal_id
            )
            return referal.partner
        except Referal.DoesNotExist:
            return None
    
    @staticmethod
    @sync_to_async
    def create_referal(partner: User, referal: User) -> Referal:
        try:
            referal = Referal.objects.prefetch_related("partner", "referal").create(
                partner=partner, referal=referal
            )
            return referal
        except Exception as e:
            return None
    