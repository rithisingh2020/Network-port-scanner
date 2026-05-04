#!/usr/bin/env python3
"""
Network Port Scanner - Cybersecurity Portfolio Project 1
Author: Rithika | RIVI Enterprises
Legal: Use ONLY on systems you own or have permission to test.
"""

import socket
import threading
import sys
from colorama import Fore, Style, init
from datetime import datetime

# கலர்ஃபுல்லாகத் தெரிய colorama-வை ஸ்டார்ட் செய்யவும்
init(autoreset=True)

# கண்டுபிடித்த ஓபன் போர்ட்களைச் சேமிக்க ஒரு லிஸ்ட்
open_ports = []
lock = threading.Lock()

def scan_port(host, port):
    """ஒரு குறிப்பிட்ட போர்ட்டைத் தட்டிப் பார்க்கும் ஃபங்ஷன்"""
    try:
        # நெட்வொர்க் கனெக்ஷன் உருவாக்க (Socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # 1 செகண்ட் வெயிட் பண்ணும்
        result = sock.connect_ex((host, port))
        
        if result == 0:  # 0 வந்தால் போர்ட் திறந்திருக்கிறது என்று அர்த்தம்
            try:
                # அந்த போர்ட்டில் என்ன சர்வீஸ் ஓடுகிறது என்று பார்க்க (eg: HTTP, SSH)
                service = socket.getservbyport(port)
            except:
                service = "Unknown"
            
            with lock:
                open_ports.append((port, service))
                print(Fore.GREEN + f'  [+] Port {port:5d} is OPEN  --> {service}')
        
        sock.close()
    except Exception:
        pass

def port_scanner(host, start_port, end_port):
    """மெயின் ஸ்கேனர் - பல திரெட்களை (Threads) ஒரே நேரத்தில் இயக்கும்"""
    print(Fore.CYAN + '=' * 55)
    print(Fore.CYAN + f'  RIVI SHIELD - NETWORK PORT SCANNER')
    print(Fore.CYAN + f'  Target IP : {host}')
    print(Fore.CYAN + f'  Port Range: {start_port} - {end_port}')
    print(Fore.CYAN + f'  Started   : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(Fore.CYAN + '=' * 55)

    threads = []
    # கொடுத்த ரேஞ்சில் உள்ள ஒவ்வொரு போர்ட்டுக்கும் ஒரு திரெட்டை உருவாக்கவும்
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(host, port))
        threads.append(t)
        t.start()

        # சிஸ்டம் லோட் ஆகாமல் இருக்க 100 100-ஆகப் பிரித்து இயக்கவும்
        if len(threads) >= 100:
            for t in threads:
                t.join()
            threads = []

    # மீதமுள்ள திரெட்களுக்காகக் காத்திருக்கவும்
    for t in threads:
        t.join()

def main():
    print(Fore.YELLOW + "\n[*] Initializing Scanner...")
    
    try:
        # உங்களிடம் விவரங்களைக் கேட்கும் பகுதி
        host = input(Fore.WHITE + "Enter the IP address to scan (e.g., 127.0.0.1): ")
        if not host:
            host = "127.0.0.1"
            
        start_port = int(input(Fore.WHITE + "Enter starting port (e.g., 1): "))
        end_port = int(input(Fore.WHITE + "Enter ending port (e.g., 1024): "))

        # ஸ்கேனரைத் தொடங்கவும்
        port_scanner(host, start_port, end_port)

        # ஸ்கேன் முடிந்த பிறகு ரிசல்ட் காட்டவும்
        print(Fore.CYAN + '=' * 55)
        print(Fore.GREEN + f'  SCAN COMPLETE!')
        print(Fore.GREEN + f'  Total Open Ports Found: {len(open_ports)}')
        print(Fore.CYAN + '=' * 55)
        
        if open_ports:
            for port, service in sorted(open_ports):
                print(Fore.GREEN + f'    Port {port} ({service})')
        else:
            print(Fore.RED + "    No open ports found in this range.")
            
    except ValueError:
        print(Fore.RED + "[!] Error: Please enter valid numbers for ports.")
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Scanner stopped by user.")
        sys.exit()

if __name__ == '__main__':
    main()
