import hashlib
import hmac
import json
import pathlib
import re
import urllib.parse

from urllib.request import Request, urlopen

import flask
from flask_babel import gettext

from searx import settings

keywords = (
    '(.*guitar|gitarre.*)',
)

author = [{
    'name': 'Justin Back',
    'url': "https://github.com/JustinBack",
}]

def execute(query):

    return {
        'answer': flask.render_template_string(loadTemplate('all')),
        'safe': True
    }

def loadTemplate(name):
    with open(str(pathlib.Path(__file__).parent.absolute()) + '/templates/' + name + '.html', 'r') as file:
        return file.read()