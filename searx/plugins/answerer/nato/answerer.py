import hashlib
import hmac
import json
import re
import html
import urllib.parse

from urllib.request import Request, urlopen

from flask_babel import gettext

from searx import settings

keywords = ('(nato) (.*)',)

author = [{
    'name': 'Justin Back',
    'url': "https://github.com/JustinBack"
}]


def answer(query):
    string = re.match(keywords[0], query, re.IGNORECASE).group(2)

    CharSet = {
        'a': 'Alfa',
        'b': 'Bravo',
        'c': 'Charlie',
        'd': 'Delta',
        'e': 'Echo',
        'f': 'Foxtrot',
        'g': 'Golf',
        'h': 'Hotel',
        'i': 'India',
        'j': 'Juliet',
        'k': 'Kilo',
        'l': 'Lima',
        'm': 'Mike',
        'n': 'November',
        'o': 'Oscar',
        'p': 'Papa',
        'q': 'Quebec',
        'r': 'Romeo',
        's': 'Sierra',
        't': 'Tango',
        'u': "Uniform",
        'v': 'Victor',
        'w': 'Whiskey',
        'x': 'X-Ray',
        'y': 'Yankee',
        'z': 'Zulu',
        '-': 'Dash',
        '.': 'Stop',
        ' ': '(space)'
    }

    string = ' '.join(CharSet.get(ele, ele) for ele in [char for char in string.lower()])

    return {
        'answer': '<b>Phonetic Alphabet (NATO):</b><br><br>' + html.escape(string).replace('(space)', '<b>(space)</b>'),
        'safe': True
    }


def self_info():
    return {'name': gettext('Nato Converter'),
            'description': gettext('Converts words into the nato phonetic alphabet'),
            'examples': ['nato Hello'],
            'bugs': {
                'text': 'Issue Tracker',
                'url': 'https://tosdr.atlassian.net/browse/TDS'
            },
            'repository': '{repository}/src/{commit}/searx/plugins/answerer/nato/answerer.py',
            'website': 'https://tosdr.org'
            }
