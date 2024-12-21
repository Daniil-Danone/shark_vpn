from typing import List, Optional
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from asgiref.sync import sync_to_async

from apps.users.models import User
from apps.tariffs.models import Tariff
from apps.configs.models import Config


class ConfigService:
   
    @staticmethod
    @sync_to_async
    def get_config(config_id: int) -> Config:
        try:
            return Config.objects.get(id=config_id)
        except Config.DoesNotExist:
            return None
    
    @staticmethod
    @sync_to_async
    def create_config(user: User, tariff: Tariff) -> Config:
        return Config.objects.create(user=user, tariff=tariff)
    
    @staticmethod
    @sync_to_async
    def update_config(config_id: int, status: str, config_name: str) -> Config:
        config = Config.objects.get(id=config_id)
        if not config:
            return
        
        if status == "done":
            now = timezone.now()

            duration_type = config.tariff.duration_type
            duration_value = config.tariff.duration_value

            if duration_type == "days":
                expiring_at = now + relativedelta(days=duration_value)
            elif duration_type == "weeks":
                expiring_at = now + relativedelta(weeks=duration_value)
            elif duration_type == "months":
                expiring_at = now + relativedelta(months=duration_value)
            elif duration_type == "years":
                expiring_at = now + relativedelta(years=duration_value)
            
            config.status = "done"
            config.payed_at = now
            config.config_name = config_name
            config.expiring_at = expiring_at.date()
            
        elif status == "cancel":
            config.status = "cancel"

        config.save()

        return config
    
    @staticmethod
    @sync_to_async
    def get_user_configs(user_id: int) -> List[Config]:
        configs = Config.objects.filter(user__user_id=user_id, config_name__isnull=False).order_by("-payed_at")
        return list(configs)
    