from typing import Dict
import psutil


def get_current_usage() -> Dict:
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    data = {
        "cpu": {
            "cores": psutil.cpu_count(logical=False),
            "threads": psutil.cpu_count(logical=True),
            "usage": sum(psutil.cpu_percent(interval=0.5, percpu=True)),
        },
        "ram": {
            "total": ram.total,
            "used": ram.used,
            "available": ram.available,
            "usage": ram.percent,
        },
        "disk": {
            "total": disk.total,
            "used": disk.used,
            "available": disk.free,
            "usage": disk.percent
        }
    }

    return data
