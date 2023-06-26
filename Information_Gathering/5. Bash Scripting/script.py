import subprocess

subnet = "192.168.50"

for host in range(1, 255):
    ip = f"{subnet}.{host}"
    result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], capture_output=True)
    if result.returncode == 0:
        print(f"Host {ip} is up")
    else:
        print(f"Host {ip} is down")
