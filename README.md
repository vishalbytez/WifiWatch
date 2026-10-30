# WifiWatch

> Discover every device on your Wi-Fi and watch live per-device bandwidth usage, right from your terminal.

**Built by Vishal** 😄

WifiWatch is a lightweight Python network tool for home and small-office networks. It answers two questions: *who is on my Wi-Fi?* and *who is using the bandwidth?*

## Features

- ARP-based device discovery across your subnet
- Shows IP address, MAC address, and hostname for each device
- Live traffic meter with per-device download, upload, and total usage
- Table sorted by heaviest user, refreshing every second
- Automatic device rescans so new devices appear while watching
- Export scan results to CSV
- Works on Windows, Linux, and macOS

## Requirements

- Python 3.9 or newer
- `scapy` and `rich` (see `requirements.txt`)
- **Windows only:** [Npcap](https://npcap.com), installed with "Install Npcap in WinPcap API-compatible mode" ticked

## Installation

```
git clone https://github.com/your-username/wifiwatch.git
cd wifiwatch
py -m pip install -r requirements.txt
```

On Linux or macOS, use `python3` and `pip3` instead of `py` and `pip`.

## Usage

Run from an **Administrator** Command Prompt on Windows, or with `sudo` on Linux/macOS.

Find your subnet with `ipconfig` (Windows) or `ip addr` (Linux). If your IPv4 address is `192.168.18.177` with mask `255.255.255.0`, your subnet is `192.168.18.0/24`.

### Scan for devices

```
py wifiwatch.py scan 192.168.18.0/24 -i "Wi-Fi"
```

Save the results to a CSV file:

```
py wifiwatch.py scan 192.168.18.0/24 -i "Wi-Fi" -o devices.csv
```

### Watch live traffic

```
py wifiwatch.py watch -i "Wi-Fi" --subnet 192.168.18.0/24
```

Press `Ctrl+C` to stop.

### Options

| Command | Option | Description |
|---------|--------|-------------|
| `scan` | `subnet` | Network to scan, for example `192.168.18.0/24` |
| `scan` | `-i`, `--iface` | Network interface name |
| `scan` | `-o`, `--output` | Save results to a CSV file |
| `watch` | `-i`, `--iface` | Network interface name (required) |
| `watch` | `--subnet` | Network to monitor (required) |
| `watch` | `--rescan` | Seconds between device rescans (default 60) |

## Important notes

- A normal PC on Wi-Fi only sees its **own** traffic. To meter every device, run `watch` on the router or gateway (Linux, OpenWrt, a Raspberry Pi acting as router) or on a machine that receives mirrored traffic.
- `scan` works from any PC on the network.
- Traffic totals reset when you close the program.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Python was not found` | Use `py` instead of `python`, or install Python from python.org and tick "Add python.exe to PATH" |
| `winpcap is not installed` | Install Npcap with WinPcap API-compatible mode, then reopen Command Prompt as Administrator |
| Scan finds nothing | Check the subnet with `ipconfig`, and pass the correct adapter name with `-i` |
| Wrong adapter | List adapters with `py -c "from scapy.all import show_interfaces; show_interfaces()"` |
| `scapy` fails to install | Use a stable Python such as 3.12 or 3.13 with `py -3.13 -m pip install -r requirements.txt` |

## Roadmap

- MAC vendor lookup (Apple, Samsung, and so on)
- Alerts when an unknown device joins
- Per-device DNS logging on a gateway
- Router API integration
- Web dashboard

## Legal

Use WifiWatch only on networks you own or have permission to administer. Scanning or monitoring networks without authorization may be illegal.

## Author

Built by **Vishal**.

## License

MIT License. Free to use, modify, and share.
