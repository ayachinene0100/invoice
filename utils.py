import re

from config import invoice_dir
from os import path
from datetime import datetime


def download_first_attach(message):
    if not message.attachments:
        return
    attach = message.attachments[0]
    with open(path.join(invoice_dir, attach['filename']), 'wb') as f:
        f.write(attach['content'].getbuffer())


def extract_date(message) -> datetime:
    """
    message.date例子：
    Mon, 09 Oct 2023 17:52:30 +0000
    Fri, 6 Oct 2023 11:40:41 -0500 (CDT)
    Thu, 05 Oct 2023 13:31:56 -0600
    Mon, 02 Oct 2023 18:46:07 +0000
    Thu, 28 Sep 2023 14:52:14 GMT
    Thu, 28 Sep 2023 11:24:43 +0800
    Mon, 25 Sep 2023 17:52:35 +0000
    Thu, 21 Sep 2023 05:14:20 +0000 (UTC)
    Thu, 21 Sep 2023 05:40:59 +0800
    Wed, 20 Sep 2023 04:40:07 +0800
    Mon, 18 Sep 2023 13:54:39 +0800 (CST)
    Mon, 18 Sep 2023 13:54:39 +0800 (GMT+08:00)
    Sat, 16 Sep 2023 13:14:50 +0800 (CST)
    Thu, 14 Sep 2023 10:06:30 -0500 (CDT)
    Tue, 12 Sep 2023 17:23:10 -0600
    Wed, 13 Sep 2023 21:22:34 +0000
    """

    s = message.date.split()[:5]
    if len(s[1]) == 1:
        s[1] = '0' + s[1]
    return datetime.strptime(' '.join(s), '%a, %d %b %Y %H:%M:%S')


def get_sender_name(message) -> str:
    return message.sent_from[0]['name']
