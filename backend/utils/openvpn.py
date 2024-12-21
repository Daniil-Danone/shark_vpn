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

        process = pexpect.spawn('./openvpn-install.sh')
        process.expect("Select an option:")
        process.sendline('1')
        process.expect("Provide a name for the client:")
        process.sendline(client_name)
        process.expect(pexpect.EOF)
        
        vpn_logger.debug(f"Конфигурация {config_file} успешно создана.")

        # command = f"sudo mv {SERVER_ROOT}{config_file} {CONFIGS_ROOT}"
        # subprocess.run(command, shell=True, check=True)

        # vpn_logger.debug(f"Конфигурация {client_name}.ovpn успешно перемещена.")

        return config_file
    
    except Exception as e:
        vpn_logger.error(f"Ошибка генерации: {e}")
        return None