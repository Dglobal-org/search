import hashlib
import hmac
import json
import re
import urllib.parse

from urllib.request import Request, urlopen

from flask_babel import gettext

from searx import settings

keywords = (
    '(.*grade.*)',
    '(.*service.*)',
    '(.*)how (secure|private|safe) is (.+)(.*)',
    '(.*)(does) (.+) care (about|for) your privacy(.*)',
    '(.*)what (grade) has (.+)(.*)',
    '(.*)(is) (.+) (secure|private|safe)(.*)'
)

author = [{
    'name': 'The ToS;DR Team',
    'url': "https://tosdr.org",
}]


def proxify(url):
    if url.startswith('//'):
        url = 'https:' + url

    if not settings.get('result_proxy'):
        return url

    url_params = dict(mortyurl=url.encode())

    if settings['result_proxy'].get('key'):
        url_params['mortyhash'] = hmac.new(settings['result_proxy']['key'],
                                           url.encode(),
                                           hashlib.sha256).hexdigest()

    return '{0}?{1}'.format(settings['result_proxy']['url'],
                            urllib.parse.urlencode(url_params))


# required answerer function
# can return a list of results (any result type) for a given query
def answer(query):
    service = ''
    matches = False

    if re.match(keywords[0], query, re.IGNORECASE):
        service = query.lower().replace('grade', '')
        service = query.lower().replace('?', '')
        matches = True
    elif re.match(keywords[1], query, re.IGNORECASE):
        service = query.lower().replace('privacy', '')
        service = query.lower().replace('?', '')
        matches = True
    elif re.match(keywords[2], query, re.IGNORECASE):
        service = query.lower().replace('service', '')
        service = query.lower().replace('?', '')
        matches = True

    if not matches:
        for index, keyword in enumerate(keywords):
            if re.match(keyword, query, re.IGNORECASE):
                try:
                    service = re.match(keywords[index], query, re.IGNORECASE).group(3)
                    matches = True
                    break
                except:
                    return False

    if not matches:
        return False

    search_result = search_service((service.strip()))

    if len(search_result) > 0:
        return {
            'answer': gettext('{service} has a Privacy {grade} on ToS;DR'.format(service=search_result['name'],
                                                                                 grade=search_result['rating'][
                                                                                     'human'])),
            'url': search_result['links']['crisp']['service'],
            'image': {
                'src': proxify(search_result['links']['crisp']['badge']['png']),
                'width': '202',
                'height': '20',
                'align': 'right'
            }
        }

    return False


def search_service(query):
    httprequest = Request('https://api.tosdr.org/search/v4/?query=' + urllib.parse.quote(query),
                          headers={"Accept": "application/json"})

    with urlopen(httprequest) as response:
        if response.status != 200:
            return []

        api = json.loads(response.read().decode())

        # Request Success
        if api['error'] & 0x100:
            if len(api["parameters"]["services"]) > 0:
                return api["parameters"]["services"][0]
            return []
        return []


def self_info():
    return {'name': gettext('ToS;DR Grade'),
            'description': gettext('Get a grade from ToS;DR using the ToS;DR API'),
            'examples': ['grade Facebook'],
            'bugs': {
                'url': 'https://tosdr.atlassian.net/browse/TDS',
                'text': 'Report a bug to the maintainer'
            },
            'website': 'https://tosdr.org',
            'repository': '{repository}/src/{commit}/searx/plugins/answerer/grade/answerer.py'
            }
