import secrets
import subprocess

from utils.logger import vpn_logger

from config.environment import SERVER_ROOT, CONFIGS_ROOT


def generate_random_client_name():
    return secrets.token_hex(nbytes=6)


def generate_vpn_config() -> str:
    try:
        client_name = generate_random_client_name()
        
        command = f"sudo ./openvpn-install.sh <<< \"add\" && echo {client_name}"
        subprocess.run(command, shell=True, check=True)

        config_file = f"{client_name}.ovpn"

        vpn_logger.debug(f"Конфигурация {config_file} успешно создана.")


        command = f"sudo mv {SERVER_ROOT}{config_file} {CONFIGS_ROOT}"
        subprocess.run(command, shell=True, check=True)

        vpn_logger.debug(f"Конфигурация {client_name}.ovpn успешно перемещена.")
        return config_file
    
    except Exception as e:
        vpn_logger.error(f"Ошибка генерации: {e}")
        return None


