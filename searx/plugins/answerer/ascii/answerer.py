import hashlib
import hmac
import json
import re
import html
import urllib.parse

from urllib.request import Request, urlopen

from flask_babel import gettext

from searx import settings

keywords = ('shrug','table flip', 'flip table', 'table unflip', 'unflip table', 'fliptable', 'unfliptable')

author = [{
    'name': 'Justin Back',
    'url': "https://github.com/JustinBack",
}]


def answer(query):

    ascii = query.split()

    if ascii[0] == 'shrug':
        return {
            'answer': '¯\_(ツ)_/¯',
        }
    elif (ascii[0] == 'table' and ascii[1] == 'flip') or (ascii[0] == 'flip' and ascii[1] == 'table') or ascii[0] == 'fliptable':
        return {
            'answer': '(╯°□°)╯︵ ┻━┻',
        }
    elif (ascii[0] == 'table' and ascii[1] == 'unflip') or (ascii[0] == 'unflip' and ascii[1] == 'table')  or ascii[0] == 'unfliptable':
        return {
            'answer': '┬─┬ノ( º _ ºノ)',
        }


def self_info():
    return {'name': gettext('Ascii Shortcuts'),
            'description': gettext('Does some Ascii Stuff'),
            'examples': ['shrug', 'table flip', 'unflip table'],
            'repository': '{repository}/src/{commit}/searx/plugins/answerer/ascii/answerer.py',
            'website': 'https://tosdr.org'
            }
