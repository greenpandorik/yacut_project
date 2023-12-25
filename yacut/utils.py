import random
import string
import re

from .models import URLMap


def get_unique_short_id():
    max_length = 6
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(max_length))


def check_symbols(url):
    if re.match("^[A-Za-z0-9]*$", url):
        return True
    return False


def check_uniq_link(short_url):
    if URLMap.query.filter_by(short=short_url).first():
        return True
    return False
