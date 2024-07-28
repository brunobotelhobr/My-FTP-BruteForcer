#!/usr/bin/python
############################################################
# Requirements:
# pip install termcolor
############################################################

from termcolor import colored
import datetime
import argparse
import time
import logging

# Disable scapy warning output
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


NAME = "FTP Brute Force Log Monitor"
VERSION = "1.0"
DATE = "02/06/2024"


ERRORS_BY_IP = {}
LOG = "/var/log/vsftpd.log"


def print_banner():
    """Print the banner."""
    print("")
    print(f"### {NAME}")
    print(f"### Version {VERSION}")
    print(f"### Date {DATE}")
    print("### by Bruno Botelho - bruno.botelho.br@gmail.com")
    print("")


def log_timestamp():
    """Return the current timestamp."""
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def main():
    """Main function."""
    print_banner()
    try:
        with open(LOG, "r") as f:  # type: ignore
            f.seek(0, 2)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                # Mon Jul  8 17:17:34 2024 [pid 7284] [anonymous] FAIL LOGIN: Client "::ffff:192.168.200.120"
                if "FAIL LOGIN" in line:
                    src = line.split(" ")[-1].replace('"', "")
                    # Remove ::ffff:
                    src = src.split(":")[-1]
                    src = src.replace("\n", "")
                    if src in ERRORS_BY_IP:
                        ERRORS_BY_IP[src] += 1
                    else:
                        ERRORS_BY_IP[src] = 1
                    print(
                        log_timestamp()
                        + f" FTP Login failed from {colored(src, 'red')} Hit count: {colored(ERRORS_BY_IP[src], 'red')}"
                    )
                # Mon Jul  8 16:58:42 2024 [pid 2316] [admin] OK LOGIN: Client "::ffff:192.168.200.120"
                if "OK LOGIN" in line:
                    src = line.split(" ")[-1].replace('"', "")
                    # Remove ::ffff:
                    src = src.split(":")[-1]
                    print(
                        log_timestamp()
                        + " FTP Login successful from "
                        + colored(src, "green")
                    )
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)
    except Exception as e:
        print(log_timestamp() + " Error reading log file: " + str(e))


if __name__ == "__main__":
    main()
