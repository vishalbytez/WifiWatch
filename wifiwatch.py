import argparse
import csv
import ipaddress
import socket
import sys
import threading
import time
from collections import defaultdict

from rich.console import Console
from rich.live import Live
from rich.table import Table
from scapy.all import ARP, IP, Ether, sniff, srp

APP_NAME = "WifiWatch"
VERSION = "1.0.0"
AUTHOR = "Vishal"

console = Console()


def banner():
    console.print(f"[bold cyan]{APP_NAME}[/bold cyan] v{VERSION}  [dim]built by {AUTHOR}[/dim]")
    console.print("[dim]Use only on networks you own or administer.[/dim]\n")


def human(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def resolve(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except OSError:
        return "-"


def scan(subnet, iface=None, timeout=3):
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=subnet)
    answered, _ = srp(packet, timeout=timeout, iface=iface, verbose=False, retry=2)
    seen = {}
    for _, reply in answered:
        seen[reply.psrc] = {"ip": reply.psrc, "mac": reply.hwsrc, "host": resolve(reply.psrc)}
    return sorted(seen.values(), key=lambda d: ipaddress.ip_address(d["ip"]))


def print_scan(devices):
    table = Table(title="Devices on your network")
    for column in ("#", "IP", "MAC", "Hostname"):
        table.add_column(column)
    for index, device in enumerate(devices, 1):
        table.add_row(str(index), device["ip"], device["mac"], device["host"])
    console.print(table)
    console.print(f"[green]{len(devices)} device(s) found[/green]")


def save_csv(devices, path):
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["ip", "mac", "host"])
        writer.writeheader()
        writer.writerows(devices)
    console.print(f"[green]Saved to {path}[/green]")


def watch(iface, subnet, rescan_every=60):
    network = ipaddress.ip_network(subnet, strict=False)
    downloaded = defaultdict(int)
    uploaded = defaultdict(int)
    lock = threading.Lock()

    def on_packet(packet):
        if IP not in packet:
            return
        src = packet[IP].src
        dst = packet[IP].dst
        size = len(packet)
        with lock:
            if ipaddress.ip_address(src) in network:
                uploaded[src] += size
            if ipaddress.ip_address(dst) in network:
                downloaded[dst] += size

    threading.Thread(
        target=lambda: sniff(iface=iface, prn=on_packet, store=False),
        daemon=True,
    ).start()

    known = {d["ip"]: d for d in scan(subnet, iface)}
    last_scan = time.time()
    started = time.time()

    def render():
        table = Table(title=f"{APP_NAME} on {iface}  |  running {int(time.time() - started)}s")
        for column in ("IP", "MAC", "Hostname", "Down", "Up", "Total"):
            table.add_column(column)
        with lock:
            ips = set(uploaded) | set(downloaded) | set(known)
            ranked = sorted(ips, key=lambda ip: uploaded[ip] + downloaded[ip], reverse=True)
            for ip in ranked:
                info = known.get(ip, {"mac": "?", "host": "-"})
                total = uploaded[ip] + downloaded[ip]
                table.add_row(
                    ip,
                    info["mac"],
                    info["host"],
                    human(downloaded[ip]),
                    human(uploaded[ip]),
                    human(total),
                )
        return table

    with Live(render(), refresh_per_second=1, console=console) as live:
        try:
            while True:
                time.sleep(1)
                if time.time() - last_scan > rescan_every:
                    known = {d["ip"]: d for d in scan(subnet, iface)}
                    last_scan = time.time()
                live.update(render())
        except KeyboardInterrupt:
            pass


def build_parser():
    parser = argparse.ArgumentParser(
        prog="wifiwatch",
        description=f"{APP_NAME} - discover devices on your Wi-Fi and meter their traffic. Built by {AUTHOR}.",
    )
    parser.add_argument("--version", action="version", version=f"{APP_NAME} {VERSION}")
    sub = parser.add_subparsers(dest="command", required=True)

    scan_cmd = sub.add_parser("scan", help="list devices on the subnet")
    scan_cmd.add_argument("subnet", help="example: 192.168.18.0/24")
    scan_cmd.add_argument("-i", "--iface", help='interface name, example: "Wi-Fi"')
    scan_cmd.add_argument("-o", "--output", help="save results to a CSV file")

    watch_cmd = sub.add_parser("watch", help="live per-device traffic meter")
    watch_cmd.add_argument("-i", "--iface", required=True, help='interface name, example: "Wi-Fi"')
    watch_cmd.add_argument("--subnet", required=True, help="example: 192.168.18.0/24")
    watch_cmd.add_argument("--rescan", type=int, default=60, help="seconds between device rescans")

    return parser


def main():
    args = build_parser().parse_args()
    banner()
    try:
        if args.command == "scan":
            devices = scan(args.subnet, args.iface)
            print_scan(devices)
            if args.output:
                save_csv(devices, args.output)
        else:
            watch(args.iface, args.subnet, args.rescan)
    except PermissionError:
        console.print("[red]Permission denied. Run as Administrator (Windows) or with sudo (Linux/macOS).[/red]")
        sys.exit(1)
    except RuntimeError as error:
        console.print(f"[red]{error}[/red]")
        console.print("[yellow]On Windows, install Npcap with WinPcap API-compatible mode enabled.[/yellow]")
        sys.exit(1)


if __name__ == "__main__":
    main()
