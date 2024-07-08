#!/usr/bin/python
############################################################
# Requirements:
# pip install scapy
# pip install termcolor
############################################################

from scapy.layers.inet import IP, TCP
from scapy.all import conf
from scapy.all import sniff
from scapy.packet import Raw
from termcolor import colored
import datetime
import logging

# Disable scapy warning output
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


NAME = "FTP Brute Force Network Monitor"
VERSION = "1.0"
DATE = "02/06/2024"
IP_FORWARD = "/proc/sys/net/ipv4/ip_forward"


ERRORS_BY_IP = {}


def print_banner():
    """Print the banner."""
    print("")
    print(f"### {NAME}")
    print(f"### Version {VERSION}")
    print(f"### Date {DATE}")
    print("### by Bruno Botelho - bruno.botelho.br@gmail.com")
    print("")


def setup():
    """Setup the environment based on provided arguments."""
    conf.verb = 0  # Disable default scapy output


def log_timestamp():
    """Return the current timestamp."""
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def ftp_mon(pkt):
    """Monitor FTP traffic."""
    src = pkt[IP].src
    try:
        load = str(pkt[Raw].load)
    except Exception:  # pylint: disable=broad-except
        load = None
    if load is not None:
        if "530 Login incorrect." in load:
            if src in ERRORS_BY_IP:
                ERRORS_BY_IP[src] += 1
            else:
                ERRORS_BY_IP[src] = 1
            print(
                log_timestamp()
                + " FTP Login failed from "
                + colored(src, "red")
                + " Hit count: "
                + colored(ERRORS_BY_IP[src], "red")
            )
        if "230 Login successful." in load:
            print(
                log_timestamp() + " FTP Login successful from " + colored(src, "green")
            )


def main():
    """Main function."""
    setup()
    print_banner()
    try:
        while True:
            sniff(prn=ftp_mon, filter="tcp port 21", store=0)
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)


if __name__ == "__main__":
    main()
