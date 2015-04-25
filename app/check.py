import hashlib
from . import config


def check_signature(signature, timestamp, nonce, echostr):
    token = config.TOKEN
    tmplist = [token, timestamp, nonce]
    tmplist.sort()
    tmpstr = "%s%s%s" % tuple(tmplist)
    tmpstr = hashlib.sha1(tmpstr.encode()).hexdigest()
    return tmpstr == signature
