from prometheus_client import Gauge


cpu_cores = Gauge(
    name="cpu_cores",
    documentation="Ядра CPU",
)

cpu_threads = Gauge(
    name="cpu_threads",
    documentation="Потоки CPU",
)

cpu_usage = Gauge(
    name="cpu_usage",
    documentation="Нагрузка на CPU",
)

ram_total = Gauge(
    name="ram_total",
    documentation="Всего RAM",
)

ram_used = Gauge(
    name="ram_used",
    documentation="Использовано RAM",
)

ram_available = Gauge(
    name="ram_available",
    documentation="Свободно RAM",
)

ram_usage = Gauge(
    name="ram_usage",
    documentation="Нагрузка на RAM",
)

disk_total = Gauge(
    name="disk_total",
    documentation="Всего DISK",
)

disk_used = Gauge(
    name="disk_used",
    documentation="Использовано DISK",
)

disk_available = Gauge(
    name="disk_available",
    documentation="Свободно DISK",
)

disk_usage = Gauge(
    name="disk_usage",
    documentation="Нагрузка на DISK",
)

configs_total = Gauge(
    name="configs_total",
    documentation="Всего конфигов",
)

configs_active = Gauge(
    name="configs_active",
    documentation="Всего активных конфигов",
)

configs_connected = Gauge(
    name="configs_connected",
    documentation="Подключенных конфигов",
)

configs_disconnected = Gauge(
    name="configs_disconnected",
    documentation="Отключенных конфигов",
)
