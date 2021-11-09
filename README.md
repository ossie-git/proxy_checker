# proxy_checker

## Table of contents

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
* [Alternatives](#alternatives)

## Introduction

**proxy_checker** is a simple Python script that takes a file with a proxy on each line in the format:

~~~
socks5://128.199.111.243:14959
https://128.199.111.243:443
http://128.199.111.243:80
~~~

and quickly verifies which are up and running by proxying requests to [HTTPBin](httpbin.org/get) and checking to see if:

* the connection was successful
* your original IP was forwarded or not

It then saves working proxies that do not leak your IP to a file of your choice in addition to displaying them on stdout.

## Installation

The only pre-requisite for this tool are Python 3 and the **requests[socks]** package. To install it with its pre-requisites:

~~~
git clone https://github.com/ossie-git/proxy_checker
cd proxy_checker
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
~~~

## Usage

Usage is straight-forward. If you do not explicitly provide a input and output file, it will default to **proxies.txt** and **live.txt**:

~~~
Usage: proxy_checker [-h] [-i INPUT] [-o OUTPUT]

Verify that list of proxies are working

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input file
  -o OUTPUT, --output OUTPUT
                        output file
~~~

By default, it queries 25 proxies concurrently. This is configurable via the **THREADS** constant. It waits for up to 20 seconds for a proxy to reply. This too is configurable via the **TIMEOUT** variable.

## Alternatives

For a quick one-liner alternative, you can use **curl**:

~~~
curl -x socks5h://localhost:8001 http://www.httpbin.org/get
curl -x https://localhost:8001 http://www.httpbin.org/get
curl -x http://localhost:8001 http://www.httpbin.org/get
~~~

There are also a number of other tools that do something similar. A GitHub search will point you in the right direction.
