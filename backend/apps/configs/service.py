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
            return Config.objects.prefetch_related("tariff").get(id=config_id)
        except Config.DoesNotExist:
            return None
    
    @staticmethod
    @sync_to_async
    def create_config(user: User, tariff: Tariff, payment_id: Optional[str] = None) -> Config:
        return Config.objects.create(user=user, tariff=tariff, payment_id=payment_id)
    
    @staticmethod
    @sync_to_async
    def get_all() -> List[Config]:
        configs = Config.objects.all()
        return list(configs)
    
    @staticmethod
    @sync_to_async
    def update_config(config_id: int, payment_status: str, config_name: Optional[str] = None) -> Config:
        config = Config.objects.get(id=config_id)
        if not config:
            return
        
        if payment_status in ["done", "balance"]:
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
            
            config.status = "enable"
            config.payment_status = payment_status
            config.payed_at = now
            config.config_name = config_name
            config.expiring_at = expiring_at.date()
            
        elif payment_status == "cancel":
            config.payment_status = "cancel"

        config.save()

        return config
    
    @staticmethod
    @sync_to_async
    def get_user_configs(user_id: int) -> List[Config]:
        configs = Config.objects.filter(user__user_id=user_id, config_name__isnull=False).order_by("-payed_at")
        return list(configs)
    
    @staticmethod
    @sync_to_async
    def get_overdue_configs() -> List[Config]:
        today = timezone.now().date()
        configs = Config.objects.prefetch_related("user").filter(status="enable", expiring_at__lt=today)
        return list(configs)
    
    @staticmethod
    @sync_to_async
    def set_disable_config(config: Config):
        config.status = "disable"
        config.save()

    @staticmethod
    @sync_to_async
    def set_connected_config(config: Config):
        config.active = "connected"
        config.save()

    @staticmethod
    @sync_to_async
    def set_disconnected_config(config: Config):
        config.active = "disconnected"
        config.save()
