from datetime import date, timedelta

from icecream import ic

from imap import imap
from listener import (
    piaotong,
    nuonuo,
    jd,
    geekbang
)
from utils import extract_date

listeners = [piaotong, nuonuo, jd, geekbang]

if __name__ == '__main__':
    messages = imap.messages(
        folder='INBOX'
    )
    # noinspection PyProtectedMember,PyTypeChecker
    messages._uid_list = reversed(messages._uid_list)

    for uid, message in messages:
        message.date = extract_date(message).date()
        if message.date < date.today() - timedelta(days=60):
            break
        ic(message.subject)
        for listener in listeners:
            listener(message)
