"""
proxy_checker is a simple Python script that takes a file with a proxy on each line in the format:

socks5://128.199.111.243:14959
https://128.199.111.243:443
http://128.199.111.243:80

and quickly verifies which are up and running by proxying requests to https://httpbin.org/get and checking to see if:

* the connection was successful
* your original IP was forwarded or not

It then saves working proxies that do not leak your IP to a file of your choice in addition to displaying them on stdout.
"""

import argparse
import json
import requests
import sys
import pkg_resources
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

TIMEOUT = 20
THREADS = 25
INPUT = "proxies.txt"
OUTPUT = "live.txt"
URL = "http://httpbin.org/get"
live = []
required_modules = ["PySocks"]


def check_deps():
    """
    checks required dependencies are installed
    """
    missing = False
    for package in required_modules:
        try:
            dist = pkg_resources.get_distribution(package)
        except pkg_resources.DistributionNotFound:
            missing = True

    if missing:
        print(
            "Missing requirements. Please run: `pip install -r requirements.txt` first"
        )
        sys.exit(1)


def fetch_real_ip():
    """
    uses http://httpbin.or/get to get our real IP and returns it
    """
    try:
        resp = requests.get(URL, timeout=TIMEOUT).text
        return json.loads(resp)["origin"]
    except:
        pass


def check_proxy(proxy, real_ip):
    """
    checks a proxy by sending to URL and checking that our real IP is not
    included in the response. Only then is it returned as a valid proxy

    :param proxy: the proxy we want to test. This is in the format:
    socks5://127.0.0.1
    :param real_ip: our real IP addres
    """
    proxies = {"http": proxy, "https": proxy}
    try:
        resp = requests.get(URL, proxies=proxies, timeout=TIMEOUT)
        if resp.status_code == 200:
            if real_ip not in resp.text:
                print(proxy)
                live.append(proxy)
    # except requests.exceptions.ConnectTimeout:
    except:
        pass


if __name__ == "__main__":
    check_deps()
    cli_parser = argparse.ArgumentParser(
        description="Check that proxies in list are working", prog="proxy_checker"
    )
    cli_parser.add_argument("-i", "--input", help="input file")
    cli_parser.add_argument("-o", "--output", help="output file")
    cli_options = cli_parser.parse_args()

    if cli_options.input:
        INPUT = cli_options.input

    if cli_options.output:
        OUTPUT = cli_options.output

    # get your real IP to check if it is leaked by the proxy
    real_ip = fetch_real_ip()

    with open(INPUT) as file:
        lines = file.readlines()
        proxy_list = [line.rstrip() for line in lines]

    with ThreadPoolExecutor(THREADS) as pool:
        for i in proxy_list:
            pool.submit(check_proxy, i, real_ip)

    with open(OUTPUT, "w") as f:
        for i in live:
            f.write("%s\n" % i)
