"""
Summary:
Script to get who scored data for individual teams

# Created by maror at 20/02/2021
"""

from betting.football import whoScored
from urllib.request import urlopen
from bs4 import BeautifulSoup
import threading
import calendar
import time
import enum
import requests
from bs4 import BeautifulSoup

call_headers = {'Content-Type': 'application/json; charset=utf-8'}

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}


def example(url):
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    print(soup.prettify())


def main():
    scr_inst = whoScored()

    example(url=scr_inst.url)

    pass


if __name__ == '__main__':
    pass