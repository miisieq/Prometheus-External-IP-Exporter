from ipaddress import IPv4Address
from prometheus_client import start_http_server, Gauge, PLATFORM_COLLECTOR, PROCESS_COLLECTOR
from prometheus_client.core import REGISTRY
import time
import requests
import os
import ipaddress
from datetime import datetime

REFRESH_TIME_SECONDS = os.getenv('REFRESH_TIME_SECONDS', 60)
REQUEST_TIMEOUT_SECONDS = os.getenv('REQUEST_TIMEOUT_SECONDS', 5)
HTTP_PORT = os.getenv('HTTP_PORT', 8080)

REGISTRY.unregister(PROCESS_COLLECTOR)
REGISTRY.unregister(PLATFORM_COLLECTOR)
REGISTRY.unregister(REGISTRY._names_to_collectors['python_gc_objects_collected_total'])

g = Gauge("external_ip", "Current external IP address", ["ip"])

def log_debug(message: str) -> None:
    current_datetime = datetime.now().isoformat(sep=" ", timespec="seconds")
    print(f"[{current_datetime}] {message}")

def get_ip() -> IPv4Address|None:
    try:
        response = requests.get("https://ifconfig.co/ip", timeout=REQUEST_TIMEOUT_SECONDS).text.strip()

        try:
            address = ipaddress.ip_address(response)

            if address.version == 4:
                log_debug(f"The correct IPv4 address \"{str(address)}\" was returned.")
                return address

        except ValueError:
            log_debug(f"The returned value \"{response}\" is not a valid IPv4 address.")

        return None
    except:
        return None

if __name__ == "__main__":
    start_http_server(HTTP_PORT)
    current_ip = None
    while True:
        ip = get_ip()
        if ip:
            g.labels(ip=ip).set(1)
        time.sleep(REFRESH_TIME_SECONDS)
