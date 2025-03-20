import pexpect
import secrets

from utils.logger import vpn_logger


def generate_random_client_name():
    return secrets.token_hex(nbytes=8)


def generate_vpn_config() -> str:
    try:
        client_name = f"shark_{generate_random_client_name()}"

        process = pexpect.spawn('./openvpn-install.sh', encoding='utf-8', timeout=60)
        
        process.expect('Select an option:')
        process.sendline('1')
        process.expect('Provide a name for the client:')
        process.sendline(client_name)

        process.expect(pexpect.EOF)
        process.close()
        
        vpn_logger.debug(f"Конфигурация {client_name} успешно создана.")

        return client_name
    
    except Exception as e:
        vpn_logger.error(f"Ошибка генерации: {e}")
        return None
    

def revoke_vpn_client(client_name: str) -> bool:
    try:
        process = pexpect.spawn('./openvpn-install.sh', encoding='utf-8', timeout=300)
        
        process.expect('Select an option:')
        process.sendline('2')

        process.expect('Select the client to revoke:')
        vpn_logger.debug(f"Вывод до expect: {process.before}")
        vpn_logger.debug(f"Вывод после expect: {process.after}")

        vpn_logger.debug(f"Список клиентов")

        process.expect('Client:')
        vpn_logger.debug(f"Вывод до expect: {process.before}")
        vpn_logger.debug(f"Вывод после expect: {process.after}")

        clients_output = process.before.strip()
        clients_list = [line.strip() for line in clients_output.splitlines()]

        vpn_logger.debug(f"Список клиентов для отзыва: {clients_list}")

        client_index = None
        for i, line in enumerate(clients_list):
            if client_name in line:
                client_index = line.split(')')[0].strip()
                break

        vpn_logger.debug(f"Клиент {client_name} найден. Номер: {client_index}")
        
        if client_index is None:
            vpn_logger.error(f"Клиент {client_name} не найден.")
            process.close()
            return False

        process.sendline(str(client_index))
        
        vpn_logger.debug(f"Ожидание подвтерждения")

        process.expect(f'Confirm {client_name} revocation\? \[y/N\]:')
        process.sendline('y')

        process.expect(pexpect.EOF, timeout=60)
        process.close()

        vpn_logger.debug(f"Клиент {client_name} успешно отозван.")
        return True

    except Exception as e:
        vpn_logger.error(f"Ошибка отзыва клиента {client_name}: {e}")
        return False