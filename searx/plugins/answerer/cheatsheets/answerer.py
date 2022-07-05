import hashlib
import hmac
import json
import pathlib
import re
import html
import urllib.parse
from os import listdir
from os.path import isdir, dirname, realpath, join

from urllib.request import Request, urlopen

import flask
from flask_babel import gettext

from searx import settings
from searx.utils import load_module

keywords = (
'(cheatsheet|cheat sheet|spickzettel|spick zettel) (.*)', '(.*) (cheatsheet|cheat sheet|spickzettel|spick zettel)')

author = [{
    'name': 'Justin Back',
    'url': "https://github.com/JustinBack"
}]


def get_cheatsheet_by_regex(string):
    cheatsheetlist = []

    for cheatsheet in cheatsheets:
        for keyword in cheatsheet['module'].keywords:
            if re.match(keyword, string, re.IGNORECASE):
                cheatsheetlist.append(cheatsheet)
    return cheatsheetlist


def answer(query):
    if re.match(keywords[0], query):
        cheatcheetName = re.match(keywords[0], query, re.IGNORECASE).group(2)
    else:
        cheatcheetName = re.match(keywords[1], query, re.IGNORECASE).group(1)

    for cheatcheet in get_cheatsheet_by_regex(cheatcheetName):
        return cheatcheet['module'].execute(query)


def loadCheatSheets():
    cheatsheets_dir = dirname(realpath(__file__)) + '/modules/'
    _cheatsheets = []

    for filename in listdir(cheatsheets_dir):
        try:
            if not isdir(join(cheatsheets_dir, filename)) or filename.startswith('_'):
                continue
            module = load_module('cheatsheet.py', join(cheatsheets_dir, filename))
            if not hasattr(module, 'keywords') or not isinstance(module.keywords, tuple) or not len(
                    module.keywords) or not hasattr(module, 'author'):
                print("Failed to load module {mod}".format(mod=filename))
                exit(99)

            moduleObj = {
                'module': module,
                'name': filename
            }
            print("Loaded Cheatsheet {mod}".format(mod=filename))
            _cheatsheets.append(moduleObj)
        except:
            print("Cheatsheet Module Error!")
    return _cheatsheets


def loadTemplate(name):
    with open(str(pathlib.Path(__file__).parent.absolute()) + '/templates/' + name + '.html', 'r') as file:
        return file.read()


def self_info():
    return {'name': gettext('Cheatsheet Index'),
            'description': gettext('Cheatsheet module to load some awesome modules found around the web.'),
            'examples': ['cheatsheet guitar'],
            'repository': '{repository}/src/{commit}/searx/plugins/answerer/cheatsheet/answerer.py',
            'website': 'https://tosdr.org'}


cheatsheets = loadCheatSheets()
