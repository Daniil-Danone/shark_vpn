import pexpect
import secrets
import subprocess

from utils.logger import vpn_logger

from config.environment import SERVER_ROOT, CONFIGS_ROOT


def generate_random_client_name():
    return secrets.token_hex(nbytes=8)


def generate_vpn_config() -> str:
    try:
        client_name = f"shark_{generate_random_client_name()}"
        config_file = f"{client_name}.ovpn"

        process = subprocess.Popen(['./openvpn-install.sh'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        process.stdin.write('1\n'.encode())
        process.stdin.write(f'{client_name}\n'.encode())
        process.stdin.flush()
        
        vpn_logger.debug(f"Конфигурация {config_file} успешно создана.")

        # command = f"sudo mv {SERVER_ROOT}{config_file} {CONFIGS_ROOT}"
        # subprocess.run(command, shell=True, check=True)

        # vpn_logger.debug(f"Конфигурация {client_name}.ovpn успешно перемещена.")

        return config_file
    
    except Exception as e:
        vpn_logger.error(f"Ошибка генерации: {e}")
        return None