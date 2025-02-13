import re
from typing import List


def parse_openvpn_logs() -> List[str]:
    try:
        connected_clients = set()
        
        connection_regex = re.compile(r"\[(\S+)\] Peer Connection Initiated with \[AF_INET\](\d+\.\d+\.\d+\.\d+):\d+")

        disconnection_regex = re.compile(r"(\S+)/(\d+\.\d+\.\d+\.\d+):\d+ Connection reset, restarting \[([^\]]+)\]")
        
        with open("syslog", 'r') as log_file:
            for line in log_file:
                connection_match = connection_regex.search(line)
                if connection_match:
                    client_name, _ = connection_match.groups()
                    connected_clients.add(client_name)
                    continue
                
                disconnection_match = disconnection_regex.search(line)
                if disconnection_match:
                    client_name, _, _ = disconnection_match.groups()
                    try:
                        connected_clients.remove(client_name)
                    except:
                        continue
        
        return list(connected_clients)
    except:
        return []
