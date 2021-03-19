# -*- coding: utf-8 -*-

from urllib.parse import quote
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urlunparse
import base64
import datetime
import hashlib
import hmac
import random


def sign_url(url, key, orig, algo="sha256", timestamp=None, nonce=None):
    parsed = urlparse(url)
    new_query = sign_query(parsed.query, key, orig, algo, timestamp, nonce)
    return urlunparse(parsed[:4] + (new_query,) + parsed[5:])


def sign_query(query, key, orig, algo="sha256", timestamp=None, nonce=None):
    if timestamp is None:
        timestamp = datetime.datetime.utcnow()
    timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    if nonce is None:
        nonce = hex(random.getrandbits(128))[2:-1]
    new_query = query
    if new_query:
        new_query += "&"
    new_query += urlencode(
        (("algo", algo), ("orig", orig), ("timestamp", timestamp), ("nonce", nonce))
    )
    signature = base64.b64encode(sign_string(new_query, str(key), algo=algo))
    new_query += "&signature=" + quote(signature)
    return new_query


def sign_string(s, key, algo="sha256", timedelta=30):
    digestmod = getattr(hashlib, algo)
    hash = hmac.HMAC(bytes(key, "utf8"), digestmod=digestmod, msg=bytes(s, "utf8"))
    return hash.digest()
