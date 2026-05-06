import socket
import threading
from queue import Queue

# Target details
target = "127.0.0.1" 
queue = Queue()
open_ports = []

def port_scan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5) 
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"[*] Port {port} is OPEN")
            open_ports.append(port)
        sock.close()
    except:
        pass

def worker():
    while not queue.empty():
        port = queue.get()
        port_scan(port)

# Ports to scan (1 to 1024)
for port in range(1, 1025):
    queue.put(port)

# Using 100 threads for maximum speed
thread_list = []
for t in range(100):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()

print(f"\nScan complete. Open ports: {open_ports}")
