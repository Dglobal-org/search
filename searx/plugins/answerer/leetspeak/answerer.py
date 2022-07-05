import hashlib
import hmac
import json
import re
import html
import urllib.parse

from urllib.request import Request, urlopen

from flask_babel import gettext

from searx import settings

keywords = ('(leet speak|leetspeak) (.*)',)

author = [{
    'name': 'J |_| 5 \'][\' 1 |\| B /-\ ( |<',
    'url': "https://github.com/JustinBack"
}]


def answer(query):
    if re.match(keywords[0], query):
        leet = re.match(keywords[0], query, re.IGNORECASE).group(2)

        leetCharSet = {
            'a': '/-\\',
            'b': '|3',
            'c': '(',
            'd': '|)',
            'e': '3',
            'f': '|=',
            'g': '6',
            'h': '|-|',
            'i': '1',
            'j': '_|',
            'k': '|<',
            'l': '|_',
            'm': '|\/|',
            'n': '|\|',
            'o': '0',
            'p': '|D',
            'q': '(,)',
            'r': '|2',
            's': '5',
            't': "']['",
            'u': '|_|',
            'v': '\/',
            'w': '\^/',
            'x': '><',
            'y': "`/",
            'z': '2'
        }

        leet = ' '.join(leetCharSet.get(ele, ele) for ele in [char for char in leet])

        return {
            'answer': leet
        }



def self_info():
    return {'name': gettext('Leetspeak Answerer'),
            'description': gettext('L 3 3 \'][\' 5 |D 3 /-\ |< I 5 C 0 0 |_'),
            'examples': ['leetspeak Hello'],
            'repository': '{repository}/src/{commit}/searx/plugins/answerer/leetspeak/answerer.py',
            'website': 'https://tosdr.org'}
