from collections import defaultdict
from os import listdir
from os.path import isdir, join, dirname, realpath
from searx.utils import load_module

from flask_babel import gettext
import re

name = gettext('Better Answerers')
description = gettext('Module to improve the Answerer functionality in searx')
default_on = True

# Self User Agent regex
p = re.compile('.*user[ -]agent.*', re.IGNORECASE)

answerers_dir = dirname(realpath(__file__)) + '/answerer/'


def load_answerers():
    answerers = []

    for filename in listdir(answerers_dir):
        try:
            if not isdir(join(answerers_dir, filename)) or filename.startswith('_'):
                continue
            module = load_module('answerer.py', join(answerers_dir, filename))
            if not hasattr(module, 'keywords') or not isinstance(module.keywords, tuple) or not len(
                    module.keywords) or not hasattr(module, 'author'):
                print("Failed to load module {mod}".format(mod=filename))
                exit(99)

            moduleObj = {
                'module': module,
                'name': filename
            }
            print("Loaded module {mod}".format(mod=filename))
            answerers.append(moduleObj)
        except Exception as Ex:
            print("Module Error!" + str(Ex))
    return answerers


def get_answerers_by_regex(string):
    answererlist = []

    for answerer in answerers:
        for keyword in answerer['module'].keywords:
            if re.match(keyword, string, re.IGNORECASE):
                answererlist.append(answerer)
    return answererlist


def get_answerers_by_keywords(answerers):
    by_keyword = defaultdict(list)
    for answerer in answerers:
        for _ in answerer['module'].keywords:
            for keyword in answerer['module'].keywords:
                by_keyword[keyword].append(answerer)
    return by_keyword


answerers = load_answerers()
answerers_by_keywords = get_answerers_by_keywords(answerers)


# attach callback to the post search hook
#  request: flask request object
#  ctx: the whole local context of the pre search hook
def post_search(request, search):
    if search.search_query.pageno > 1:
        return True

    for answerer in get_answerers_by_regex(search.search_query.query):
        result = answerer['module'].answer(search.search_query.query)

        if result:
            result['author'] = answerer['module'].author
            result['info'] = answerer['module'].self_info()

            search.result_container.answers[answerer['name']] = result

    return True
