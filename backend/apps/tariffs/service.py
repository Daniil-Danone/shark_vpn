from typing import List, Optional
from asgiref.sync import sync_to_async

from apps.tariffs.models import Tariff


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
    