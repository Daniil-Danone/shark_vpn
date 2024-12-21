import os
import secrets
from subprocess import run

from utils.logger import vpn_logger

from config.environment import SERVER_ROOT, CONFIGS_ROOT


def generate_random_name() -> str:
    return secrets.token_hex(nbytes=8)


def generate_vpn_config() -> str:
    try:
        random_name = f"shark_{generate_random_name()}"
        config_name = f"{random_name}.ovpn"
        config_path = os.path.join(CONFIGS_ROOT, f"{config_name}.ovpn")

        command = (
            f"docker exec openvpn-server "
            f"easyrsa build-client-full {random_name} nopass && "
            f"docker exec openvpn-server "
            f"ovpn_getclient {random_name} > {config_path}"
        )
        
        run(command, shell=True, check=True)

        vpn_logger.debug(f"Конфигурация {config_name} успешно создана.")

        return config_name
    
    except Exception as e:
        vpn_logger.error(f"Ошибка генерации: {e}")
        return None
