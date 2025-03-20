from typing import Dict, List, Optional
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from asgiref.sync import sync_to_async

from apps.users.models import User
from apps.tariffs.models import Receipt, Tariff
from apps.configs.models import Config


class ConfigService:

    @staticmethod
    @sync_to_async
    def get_all() -> List[Config]:
        configs = Config.objects.all()
        return list(configs)
    
    @staticmethod
    @sync_to_async
    def get_config(config_id: int) -> Config:
        try:
            return Config.objects.prefetch_related("tariff").get(id=config_id)
        except Config.DoesNotExist:
            return None
    
    @staticmethod
    @sync_to_async
    def get_user_configs(user_id: int) -> List[Config]:
        now = timezone.now().date()
        configs = Config.objects.filter(
            user__user_id=user_id, expiring_at__gte=now
        ).prefetch_related("tariff", "user").order_by("-created_at")
        return list(configs)
    
    @staticmethod
    @sync_to_async
    def get_overdue_configs() -> List[Config]:
        today = timezone.now().date()
        configs = Config.objects.prefetch_related("tariff", "user").filter(status="enable", expiring_at__lt=today)
        return list(configs)
    
    @staticmethod
    @sync_to_async
    def create_config(user: User, tariff: Tariff, receipt: Receipt, config_name: str) -> Config:
        now = timezone.now()

        duration_type = tariff.duration_type
        duration_value = tariff.duration_value

        if duration_type == "days":
            expiring_at = now + relativedelta(days=duration_value)
        elif duration_type == "weeks":
            expiring_at = now + relativedelta(weeks=duration_value)
        elif duration_type == "months":
            expiring_at = now + relativedelta(months=duration_value)
        elif duration_type == "years":
            expiring_at = now + relativedelta(years=duration_value)
        
        return Config.objects.create(
            user=user, tariff=tariff, receipt=receipt, config_name=config_name, expiring_at=expiring_at
        )

    @staticmethod
    @sync_to_async
    def update_config(config_id: int, data: Dict) -> bool:
        try:
            Config.objects.filter(id=config_id).update(**data)
            return True
        except Config.DoesNotExist:
            return False
        except Exception as e:
            return False