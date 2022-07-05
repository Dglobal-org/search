import hashlib
import hmac
import json
import re
import html
import urllib.parse

from urllib.request import Request, urlopen

from flask_babel import gettext

from searx import settings

keywords = ('(md5|sha256|sha512|md4|sha1) (.*)',)

author = [{
    'name': 'Justin Back',
    'url': "https://github.com/JustinBack"
}, {
    'name': 'Searx',
    'url': "https://github.com/searx",
    'title': 'Original Code'
}]


def answer(query):
    algo = re.match(keywords[0], query, re.IGNORECASE).group(1).lower()
    string = re.match(keywords[0], query, re.IGNORECASE).group(2)

    if algo == 'md5':
        hash = md5(string)
    elif algo == 'sha256':
        hash = sha256(string)
    elif algo == 'sha512':
        hash = sha512(string)
    elif algo == 'sha1':
        hash = sha1(string)
    elif algo == 'md4':
        hash = md4(string)
    else:
        hash = 'Unable to calculate hash, {algo} is an unsupported algorithm'.format(algo=algo)

    return {
        'answer': '{algo} digested hex hash: {hash} '.format(hash=hash, algo=algo)
    }


def md5(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()


def sha256(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


def sha512(string):
    return hashlib.sha512(string.encode('utf-8')).hexdigest()


def sha1(string):
    return hashlib.sha1(string.encode('utf-8')).hexdigest()


def md4(string):
    return hashlib.new('md4', string.encode('utf-8')).hexdigest()


def self_info():
    return {'name': gettext('Hash Generator'),
            'description': gettext('Generate md4, md5, sha1, sha256 and sha512 hashes'),
            'examples': ['sha256 My String'],
            'repository': '{repository}/src/{commit}/searx/plugins/answerer/hash/answerer.py',
            'website': 'https://tosdr.org'
            }
