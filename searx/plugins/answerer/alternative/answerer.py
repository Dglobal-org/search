import hashlib
import hmac
import json
import pathlib
import re
import urllib.parse
from concurrent.futures import __dir__

from urllib.request import Request, urlopen

import flask
from flask_babel import gettext

from searx import settings

keywords = (
    '(alternative to) (.+)(?:[?]?)',
    '(alternative) (.+)(?:[?]?)',
    '(.+) (alternative)(?:[?]?)',
    '(what is|whats|what\'s) an alternative to (.+)(?:[?]?)',
)

author = [{
    'name': gettext('The ToS;DR Team'),
    'url': "https://tosdr.org",
}]




def answer(query):
    service = ''
    matches = False


    if re.match(keywords[2], query, re.IGNORECASE):
        service = query.lower().replace('alternative', '')
        service = query.lower().replace('?', '')
        matches = True
    elif not matches:
        for index, keyword in enumerate(keywords):
            if re.match(keyword, query):
                try:
                    service = re.match(keywords[index], query, re.IGNORECASE).group(2)
                    matches = True
                    break
                except:
                    return False

    if not matches:
        return False

    _alternatives = searchAlternatives(service.strip())

    if not _alternatives:
        return False

    return {
        'answer': flask.render_template_string(loadTemplate('answer'), alternatives= _alternatives, original= service.strip()),
        'safe': True,
    }


def loadTemplate(name):
    with open(str(pathlib.Path(__file__).parent.absolute()) + '/templates/' + name + '.html', 'r') as file:
        return file.read()


def searchAlternatives(service):
    service = service.lower()
    if service in alternatives:
        if alternatives[service] is bool:
            return False
        return alternatives[service]
    return False


def loadAlternatives():
    with open(str(pathlib.Path(__file__).parent.absolute()) + '/shared/alternatives.json', 'r') as file:
        data = file.read()
        return json.loads(data)


def self_info():
    return {'name': gettext('Privacy Alternative'),
            'description': gettext('Get privacy friendly alternatives from popular services.'),
            'examples': ['alternative google'],
            'bugs': {
                'url': 'https://tosdr.atlassian.net/browse/TDS',
                'text': gettext('Report a bug to the maintainer')
            },
            'website': 'https://tosdr.org',
            'repository': '{repository}/src/{commit}/searx/plugins/answerer/alternative/answerer.py'
            }


alternatives = loadAlternatives()
