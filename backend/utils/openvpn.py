import pexpect
import secrets

from utils.logger import vpn_logger


def generate_random_client_name():
    return secrets.token_hex(nbytes=8)


def generate_vpn_config() -> str:
    try:
        client_name = f"shark_{generate_random_client_name()}"
        config_file = f"{client_name}.ovpn"

        process = pexpect.spawn('./openvpn-install.sh')
        process.expect('Select an option:')
        process.sendline('1')
        process.expect('Provide a name for the client:')
        process.sendline(client_name)

        process.expect(pexpect.EOF)
        process.close()
        
        vpn_logger.debug(f"Конфигурация {config_file} успешно создана.")

        return config_file
    
    except Exception as e:
        vpn_logger.error(f"Ошибка генерации: {e}")
        return None