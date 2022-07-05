import hashlib
import hmac
import json
import re
import html
import urllib.parse

from urllib.request import Request, urlopen

from flask_babel import gettext

from searx import settings

keywords = ('^https?\:\/\/([\w\-\.]+\.onion)(.*)',)

author = [{
    'name': 'Justin Back',
    'url': "https://github.com/JustinBack",
}]


def answer(query):
    onion = re.match(keywords[0], query).group(1)

    return {
        'answer': 'You are trying to reach an onion/hidden service.<br><br>To access {onion} you will have to use the Tor Browser.'.format(
            onion=html.escape(onion)),
        'safe': True,
        'button': {
            'url': 'https://www.torproject.org/projects/torbrowser.html.en#downloads',
            'text': 'Download Tor',
            'icon': 'download',
            'position': 'bottom',
            'target': '_blank'
        }
    }


def self_info():
    return {'name': gettext('Onion Notice'),
            'description': gettext('Give a notice if an onion address has been queried'),
            'examples': ['http://6tc72lnilgt4dn2u6qk44vfns2qca552smajbilfcl6zs7ezf7emhbad.onion'],
            'repository': '{repository}/src/{commit}/searx/plugins/answerer/onion/answerer.py',
            'website': 'https://tosdr.org'
            }
