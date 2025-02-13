from typing import Optional
from asgiref.sync import sync_to_async

from apps.users.models import User

from config.environment import REFERAL_BONUS, PARTNER_BONUS

class UserService:
    @staticmethod
    @sync_to_async
    def get_user(user_id: int) -> User:
        try:
            return User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return None
        
    @staticmethod
    @sync_to_async
    def create_user(user_id: int, full_name: str, username: Optional[str] = None) -> User:
        return User.objects.create(
            user_id=user_id, full_name=full_name, username=username
        )
    
    @staticmethod
    @sync_to_async
    def accure_referal_bonuses(referal: User) -> User:
        referal.earned = round(referal.earned + REFERAL_BONUS, 2)
        referal.balance = round(referal.balance + REFERAL_BONUS, 2)
        referal.save()

        return referal
    
    @staticmethod
    @sync_to_async
    def accure_partner_bonuses(partner: User) -> User:
        partner.earned = round(partner.earned + PARTNER_BONUS, 2)
        partner.balance = round(partner.balance + PARTNER_BONUS, 2)
        partner.save

    @staticmethod
    @sync_to_async
    def accure_bonuses(partner: User, amount: int) -> User:
        partner.earned = round(partner.earned + amount, 2)
        partner.balance = round(partner.balance + amount, 2)
        partner.save
    
    @staticmethod
    @sync_to_async
    def accure_balance(user: User, amount: float) -> User:
        user.balance = round(user.balance + amount, 2)
        user.save()
        
        return user
    
    @staticmethod
    @sync_to_async
    def writeoff_balance(user: User, amount: float) -> User:
        user.balance = round(user.balance - amount, 2)
        user.save()

        return user