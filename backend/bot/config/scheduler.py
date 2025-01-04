from typing import Dict
from django.utils import timezone
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from utils import openvpn, system_core
from utils.logger import scheduler_logger

from apps.configs.service import ConfigService

from config.settings import TIME_ZONE

from bot.config import messages, metric
from bot.config.sessions import bot, asyncio_scheduler


async def delete_task_by_job_id(job_id: str):
    previous_job = asyncio_scheduler.get_job(job_id=job_id)
    if previous_job:
        asyncio_scheduler.remove_job(job_id=job_id)
        scheduler_logger.debug(f"[DELETE JOB] Job {job_id} deleted")


async def check_overdue_configs():
    overdue_configs = await ConfigService.get_overdue_configs()

    for overdue_config in overdue_configs:
        try:
            await ConfigService.set_disable_config(config=overdue_config)
            await openvpn.revoke_vpn_client(client_name=overdue_config.config_name)
            await bot.send_message(
                chat_id=overdue_config.user.user_id,
                text=messages.CONFIG_OVERDUED.format(
                    config_name=f"{overdue_config.config_name}.ovpn"
                )
            )
            scheduler_logger.debug(f"[OVERDUE] Config {overdue_config.config_name} revoked!")
        except Exception as e:
            scheduler_logger.error(f"[OVERDUE] Error: {e}")


async def update_metric():
    system_stat = system_core.get_current_usage()

    cpu_stat: Dict[str, float] = system_stat.get("cpu")
    ram_stat: Dict[str, float] = system_stat.get("ram")
    disk_stat: Dict[str, float] = system_stat.get("disk")

    metric.cpu_cores.set(cpu_stat.get("cores"))
    metric.cpu_threads.set(cpu_stat.get("threads"))
    metric.cpu_usage.set(cpu_stat.get("usage"))

    metric.ram_total.set(ram_stat.get("total"))
    metric.ram_used.set(ram_stat.get("used"))
    metric.ram_available.set(ram_stat.get("available"))
    metric.ram_usage.set(ram_stat.get("usage"))

    metric.disk_total.set(disk_stat.get("total"))
    metric.disk_used.set(disk_stat.get("used"))
    metric.disk_available.set(disk_stat.get("available"))
    metric.disk_usage.set(disk_stat.get("usage"))
    

async def setup_scheduler_jobs():
    asyncio_scheduler.add_job(
        check_overdue_configs,
        trigger=CronTrigger(hour=0, minute=0, second=0, timezone=TIME_ZONE)
    )
    asyncio_scheduler.add_job(
        update_metric,
        trigger=IntervalTrigger(seconds=10, timezone=TIME_ZONE)
    )
