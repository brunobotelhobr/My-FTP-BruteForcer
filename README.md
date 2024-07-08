# My-FTP-BruteForcer 
POC: Python implementation of a FTP Brute Force Utility.

This uses Python 3.
To install the requirements:
````
pip install -r requirements.txt
`````

## Attack: Attack
```
python bruteforcer.py --help
usage: bruteforcer.py [-h] -t--target TARGET [-p PORT] -u USER_LIST -P PASSWORD_LIST

options:
  -h, --help            show this help message and exit
  -t--target TARGET     [Required] Target IP address or hostname.
  -p PORT, --port PORT  Port to connect to. Default is 21.
  -U USER_LIST, --user-list USER_LIST
                        [Required] File containing usernames to test.
  -P PASSWORD_LIST, --password-list PASSWORD_LIST
                        [Required] File containing passwords to test.
```

Example:
```
python bruteforcer.py -t 192.168.200.100 -U /root/Wordlist/userlist.txt -P /root/Wordlist/pass.txt
```

## Detect: Network
```
ftp-bruteforce-network-monitor.py
```

Example:
```
python ftp-bruteforce-network-monitor.py
```

## Detect: VSFTP Log
```
ftp-bruteforce-log-monitor.py
```

Example:
```
python ftp-bruteforce-log-monitor.py
```
