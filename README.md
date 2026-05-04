# Network Port Scanner

A multi-threaded Python port scanner for network security assessment.

## Features
- Multi-threaded scanning (100x faster than single-thread)
- Service name detection (SSH, HTTP, FTP etc)
- Color-coded output
- Configurable port ranges

## Installation
```bash
git clone https://github.com/yourusername/network-port-scanner
cd network-port-scanner
pip3 install colorama
```

## Usage
```bash
python3 scanner.py              # Scan localhost
python3 scanner.py 127.0.0.1 1 1024
```

## Screenshots
![Port Scanner Output](screenshots/scan_output.png)

## Legal Notice
For educational use only. Use on authorized systems only.
