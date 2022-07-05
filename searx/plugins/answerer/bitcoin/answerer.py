import hashlib
import hmac
import json
import pathlib
import re
import html
import urllib.parse

from urllib.request import Request, urlopen

import flask
from flask_babel import gettext

from searx import settings

keywords = ('(bitcoin|btc|BTC) (.{3})(.*)', '(bitcoin|btc|BTC)')

author = [{
    'name': 'Justin Back',
    'url': "https://github.com/JustinBack"
}]


def answer(query):
    if re.match(keywords[0], query, re.IGNORECASE):

        currency = re.match(keywords[0], query, re.IGNORECASE).group(2)
        api = lookup_currency(currency)

        if not api:
            return False

        return {
            'answer': flask.render_template_string(loadTemplate('currency'),
                                                   usd=html.escape(str((api['bpi']['USD']['rate_float'])) + ' USD'),
                                                   currency_value=html.escape(
                                                       str(api['bpi'][currency]['rate_float']) + ' ' + currency),
                                                   currency=html.escape(currency),
                                                   disclaimer=html.escape(str((api['disclaimer']))),
                                                   ),
            'safe': True
        }

    else:
        api = lookup_top()

        if not api:
            return False

        return {
            'answer': flask.render_template_string(loadTemplate('all'),
                                                   usd=html.escape('$' + str((api['bpi']['USD']['rate_float']))),
                                                   eur=html.escape(str(api['bpi']['EUR']['rate_float']) + 'â‚¬'),
                                                   gbp=html.escape(str(api['bpi']['USD']['rate_float']) + 'Â£'),
                                                   disclaimer=html.escape(str((api['disclaimer']))),
                                                   ),
            'safe': True
        }


def loadTemplate(name):
    with open(str(pathlib.Path(__file__).parent.absolute()) + '/templates/' + name + '.html', 'r') as file:
        return file.read()


def lookup_top():
    httprequest = Request('https://api.coindesk.com/v1/bpi/currentprice.json',
                          headers={"Accept": "application/json"})

    with urlopen(httprequest) as response:
        if response.status != 200:
            return False

        api = json.loads(response.read().decode())

        return api


def lookup_currency(currency):
    try:
        httprequest = Request('https://api.coindesk.com/v1/bpi/currentprice/' + urllib.parse.quote(currency) + '.json',
                              headers={"Accept": "application/json"})

        with urlopen(httprequest) as response:
            if response.status != 200:
                return False

            api = json.loads(response.read().decode())

            return api
    except:
        return False


def self_info():
    return {'name': gettext('Bitcoin Index'),
            'description': gettext('Get a the bitcoin index via currency or by default via USD, EUR and GBP'),
            'examples': ['bitcoin EUR', 'bitcoin', 'btc EUR', 'btc'],
            'repository': '{repository}/src/{commit}/searx/plugins/answerer/bitcoin/answerer.py',
            'website': 'https://tosdr.org'}
