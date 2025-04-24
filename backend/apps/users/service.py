from typing import Optional, List
from django.db.models import F
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
    def get_users() -> List[User]:
        return list(User.objects.all())

        
    @staticmethod
    @sync_to_async
    def create_user(user_id: int, full_name: str, username: Optional[str] = None) -> User:
        return User.objects.create(
            user_id=user_id, full_name=full_name, username=username
        )

    @staticmethod
    @sync_to_async
    def accure_bonuses(user_id: int, amount: int) -> bool:
        try:
            User.objects.filter(user_id=user_id).update(
                earned=round(F('earned') + amount, 2),
                balance=round(F('balance') + amount, 2)
            )
            return True
        except User.DoesNotExist:
            return False
        except Exception as e:
            return False
    
    @staticmethod
    @sync_to_async
    def accure_balance(user_id: int, amount: float) -> bool:
        try:
            User.objects.filter(user_id=user_id).update(
                balance=round(F('balance') + amount, 2)
            )
            return True
        except User.DoesNotExist:
            return False
        except Exception as e:
            return False
    
    @staticmethod
    @sync_to_async
    def writeoff_balance(user_id: int, amount: float) -> bool:
        try:
            User.objects.filter(user_id=user_id).update(
                balance=round(F('balance') - amount, 2)
            )
            return True
        except User.DoesNotExist:
            return False
        except Exception as e:
            return False