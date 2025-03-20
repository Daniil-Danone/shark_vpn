import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


# PostgreSQL
POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT")
POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")

# Redis
REDIS_HOST: str = os.getenv("REDIS_HOST")
REDIS_PORT: str = os.getenv("REDIS_PORT")
REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")

# Telegram
BOT_TOKEN: str = os.environ.get("BOT_TOKEN")
ADMIN_CHAT_ID: int = os.environ.get("ADMIN_CHAT_ID")

ITEMS_PER_PAGE: int = 6

CONFIGS_DIR: Path = BASE_DIR / "openvpn_configs"

REFERAL_BONUS: float = 50.00
PARTNER_BONUS: float = 50.00

# Constants
SERVER_ROOT: str = "/root"
CONFIGS_ROOT: str = "/root/vpn_bot/openvpn_configs"
ADMIN_PANEL_LINK: str = "https://sharkvpn.ledokol.it/admin"

# YouKassa URLS
INIT_PAYMENT_URL: str = "https://api.yookassa.ru/v3/payments"
CHECK_PAYMENT_STATUS_URL: str = "https://api.yookassa.ru/v3/payments/{payment_id}"
CANCEL_PAYMENT_URL: str = "https://api.yookassa.ru/v3/payments/{payment_id}/cancel"

# YouKassa Credentials
CLIENT_ID: str = os.environ.get("YOUKASSA_CLIENT_ID")
REDIRECT_URL: str = os.environ.get("YOUKASSA_REDIRECT_URL")
CLIENT_SECRET: str = os.environ.get("YOUKASSA_CLIENT_SECRET")

# YouKassa Statuses
SUCCEEDED: str = "succeeded"
CANCELED: str = "canceled"