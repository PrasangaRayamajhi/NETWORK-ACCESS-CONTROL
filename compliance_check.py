import paramiko
import time
import logging
 
logging.basicConfig(filename='/var/log/compliance_check.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
 
def check_os(ip, username):
    password = "client1" if username == "client1" else "client2"
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password, timeout=5)
        stdin, stdout, stderr = client.exec_command('lsb_release -d')
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        client.close()
        if error:
            logging.error(f"Error checking {ip}: {error}")
            return False
        logging.info(f"OS check for {ip}: {output}")
        return "20.04" in output or "22.04" in output
    except Exception as e:
        logging.error(f"Failed to connect to {ip}: {str(e)}")
        return False
 
while True:
    clients = {"192.168.56.101": "client1", "192.168.56.102": "client2"}
    for ip, user in clients.items():
        status = "compliant" if check_os(ip, user) else "non-compliant"
        with open(f"/tmp/{user}_status", "w") as f:
            f.write(status)
        logging.info(f"Updated status for {user} ({ip}): {status}")
    time.sleep(60)