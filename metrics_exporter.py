import re
import time
from prometheus_client import start_http_server, Gauge
import logging
 
logging.basicConfig(filename='/var/log/metrics_exporter.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
 
# Prometheus metrics
compliant_devices = Gauge('nac_compliant_devices', 'Number of compliant devices')
non_compliant_devices = Gauge('nac_non_compliant_devices', 'Number of non-compliant devices')
authenticated_devices = Gauge('nac_authenticated_devices', 'Number of authenticated devices')
non_authenticated_devices = Gauge('nac_non_authenticated_devices', 'Number of non-authenticated devices')
os_version = Gauge('nac_os_version', 'OS version of compliant devices', ['client', 'os_version'])
 
def parse_compliance_status():
    clients = {"client1": "192.168.56.101", "client2": "192.168.56.102"}
    compliant_count = 0
    non_compliant_count = 0
    for client, ip in clients.items():
        try:
            with open(f"/tmp/{client}_status", "r") as f:
                status = f.read().strip()
                if status == "compliant":
                    compliant_count += 1
                else:
                    non_compliant_count += 1
        except Exception as e:
            logging.error(f"Error reading status for {client}: {str(e)}")
            non_compliant_count += 1
    compliant_devices.set(compliant_count)
    non_compliant_devices.set(non_compliant_count)
 
def parse_os_versions():
    clients = {"client1": "192.168.56.101", "client2": "192.168.56.102"}
    os_pattern = re.compile(r'OS check for .*?: Description:\s+(.+?)$')
    try:
        with open("/var/log/compliance_check.log", "r") as f:
            log_content = f.read()
            matches = os_pattern.findall(log_content)
            for client, ip in clients.items():
                os_ver = "unknown"
                for match in matches:
                    if ip in log_content:
                        os_ver = match.strip()
                        break
                # Only set for compliant devices
                with open(f"/tmp/{client}_status", "r") as f:
                    if f.read().strip() == "compliant":
                        os_version.labels(client=client, os_version=os_ver).set(1)
                    else:
                        os_version.labels(client=client, os_version=os_ver).set(0)
    except Exception as e:
        logging.error(f"Error parsing OS versions: {str(e)}")
 
def parse_authentication_status():
    clients = {"client1": "192.168.56.101", "client2": "192.168.56.102"}
    auth_count = 0
    non_auth_count = 0
    try:
        with open("/var/log/freeradius/radius.log", "r") as f:
            log_content = f.read()
            for client in clients:
                if f"Login OK: [{client}]" in log_content:
                    auth_count += 1
                else:
                    non_auth_count += 1
    except Exception as e:
        logging.error(f"Error parsing radius log: {str(e)}")
        non_auth_count += 2  # Assume both non-authenticated if log unavailable
    authenticated_devices.set(auth_count)
    non_authenticated_devices.set(non_auth_count)
 
if __name__ == "__main__":
    start_http_server(8000)  # Expose metrics on port 8000
    while True:
        try:
            parse_compliance_status()
            parse_os_versions()
            parse_authentication_status()
            logging.info("Metrics updated")
        except Exception as e:
            logging.error(f"Error updating metrics: {str(e)}")
        time.sleep(30)  # Update every 30 seconds