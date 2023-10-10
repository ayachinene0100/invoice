import re
from os import path
from uuid import uuid4

import orjson
import requests
from bs4 import BeautifulSoup

from browser import browser
from config import invoice_dir
from utils import download_first_attach
from utils import get_sender_name


def piaotong(message):
    if get_sender_name(message) != '票通':
        return
    download_first_attach(message)


def nuonuo(message):
    if get_sender_name(message) != '诺诺网':
        return
    soup = BeautifulSoup(message.body['html'][0], 'html.parser')
    download_url = soup.find('a', string='点击下载发票').attrs['href']
    with browser.new_page() as p:
        p.goto(download_url)
        with p.expect_download() as download:
            p.locator('a:has-text("下载PDF文件")').click()
        pdf = download.value
        pdf.save_as(path.join(invoice_dir, pdf.suggested_filename))


def jd(message):
    if get_sender_name(message) != '京东JD.com':
        return
    soup = BeautifulSoup(message.body['plain'][0], 'html.parser')
    download_url = soup.find('a', string='发票PDF文件下载').attrs['href']
    with open(path.join(invoice_dir, str(uuid4()) + '.pdf'), 'wb') as f:
        f.write(requests.get(download_url).content)


def geekbang(message):
    if get_sender_name(message) != '极客邦科技':
        return
    soup = BeautifulSoup(message.body['plain'][0], 'html.parser')
    download_url = soup.find('p', string=re.compile('http')).text
    with open(path.join(invoice_dir, str(uuid4()) + '.pdf'), 'wb') as f:
        pdf_url = orjson.loads(requests.get(download_url).content)['data']['link']
        f.write(requests.get(pdf_url).content)

