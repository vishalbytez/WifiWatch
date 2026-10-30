# WifiWatch

> Discover devices on your local network and inspect network traffic from your terminal.

**Built by Vishal.hehe**

WifiWatch is a lightweight Python network utility for home and small-office networks. It helps answer two questions: *which devices are visible on my local network?* and *what traffic can this machine observe for those devices?*

## Features

- ARP-based device discovery across an IPv4 subnet
- Displays each discovered device's IP address, MAC address, and reverse-resolved hostname (when available)
- Live traffic counters for observed upload and download packets, grouped by local IP address
- Terminal table ranked by observed traffic and refreshed every second
- Periodic rescans while monitoring so newly discovered devices can be listed
- Export device scan results to CSV
- Designed for Windows, Linux, and macOS (packet-capture setup differs by platform)

## Requirements

- Python 3.9 or newer
- Dependencies listed in `requirements.txt` (`scapy` and `rich`)
- **Windows:** [Npcap](https://npcap.com/) installed with **WinPcap API-compatible mode** enabled
- **Linux/macOS:** packet-capture support from the platform (typically libpcap); administrator/root privileges may be required

## Installation

Clone the repository:

```bash
git clone https://github.com/isthisvishal/WifiWatch.git
cd WifiWatch
```

Install Python dependencies.

**Windows (PowerShell):**

```powershell
py -m pip install -r requirements.txt
```

**Linux/macOS:**

```bash
python3 -m pip install -r requirements.txt
```

## Usage

Run packet operations from an **Administrator** terminal on Windows, or with `sudo` on Linux/macOS.

First, identify your local IPv4 subnet. On Windows, use `ipconfig`; on Linux, use `ip addr`. For example, an address of `192.168.18.177` with subnet mask `255.255.255.0` normally corresponds to `192.168.18.0/24`.

### Scan for devices

**Windows:**

```powershell
py wifiwatch.py scan 192.168.18.0/24 -i "Wi-Fi"
```

**Linux:**

```bash
sudo python3 wifiwatch.py scan 192.168.18.0/24 -i wlan0
```

**macOS:**

```bash
sudo python3 wifiwatch.py scan 192.168.18.0/24 -i en0
```

Save scan results to CSV:

```powershell
py wifiwatch.py scan 192.168.18.0/24 -i "Wi-Fi" -o devices.csv
```

### Watch observed traffic

**Windows:**

```powershell
py wifiwatch.py watch -i "Wi-Fi" --subnet 192.168.18.0/24
```

**Linux:**

```bash
sudo python3 wifiwatch.py watch -i wlan0 --subnet 192.168.18.0/24
```

Press `Ctrl+C` to stop monitoring.

> **Traffic visibility limitation:** On a typical switched Ethernet or Wi-Fi network, a computer generally cannot see other devices' unicast traffic. The live counters only reflect packets visible to the capture interface; they are not guaranteed to represent each device's total internet usage. For network-wide per-device monitoring, run the capture at the router/gateway or use a properly configured mirrored traffic source. Wi-Fi client isolation, access-point behavior, and operating-system capture support can also affect visibility.

### Options

| Command | Option | Description |
|---------|--------|-------------|
| `scan` | `subnet` | IPv4 network to scan, for example `192.168.18.0/24` |
| `scan` | `-i`, `--iface` | Network interface name |
| `scan` | `-o`, `--output` | Save results to a CSV file |
| `watch` | `-i`, `--iface` | Capture interface name (required) |
| `watch` | `--subnet` | Local IPv4 subnet to track (required) |
| `watch` | `--rescan` | Seconds between device rescans (default: 60) |

## Troubleshooting

| Problem | What to try |
|---------|-------------|
| Python is not found on Windows | Use `py`, or install Python from [python.org](https://www.python.org/downloads/) and enable **Add Python to PATH** |
| Scapy reports a missing capture driver on Windows | Install [Npcap](https://npcap.com/) with WinPcap API-compatible mode enabled, then reopen an Administrator terminal |
| Scan finds no devices | Confirm the subnet and subnet mask, check that the target devices are on the same local network, and select the correct interface |
| Wrong or unknown interface | On Windows, run `py -c "from scapy.all import show_interfaces; show_interfaces()"`; on Linux, inspect interfaces with `ip link` |
| Permission or capture error | Run the terminal with Administrator/root privileges and confirm packet-capture support is installed |
| Dependency installation fails | Try a supported Python release such as Python 3.12 or 3.13, then reinstall with `py -3.13 -m pip install -r requirements.txt` on Windows |

## Roadmap

- MAC vendor lookup (for example, Apple, Samsung, and other manufacturers)
- Alerts when an unknown device appears
- Per-device DNS logging when running at a suitable gateway/capture point
- Router and access-point API integration
- Web dashboard

## Legal

Use WifiWatch only on networks you own or are authorized to administer. Scanning or monitoring networks without permission may violate applicable laws or network policies.

## Author

Built by **Vishal.hehe**.

## License

MIT License. Free to use, modify, and share.
