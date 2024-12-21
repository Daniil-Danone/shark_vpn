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

# Telegram
BOT_TOKEN: str = os.environ.get("BOT_TOKEN")

ITEMS_PER_PAGE: int = 6

CONFIGS_DIR: Path = BASE_DIR / "openvpn_configs"

REFERAL_BONUS: float = 100.00


# Constants
SERVER_ROOT: str = "/root"
CONFIGS_ROOT: str = "/root/vpn_bot/openvpn_configs"