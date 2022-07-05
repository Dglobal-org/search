from functools import reduce
from operator import mul

from flask_babel import gettext


keywords = ('min',
            'max',
            'avg',
            'sum',
            'prod')

author = {
    'name': 'Searx Core',
    'url': "https://github.com/searx/searx"
}

# required answerer function
# can return a list of results (any result type) for a given query
def answer(query):
    parts = query.query.split()

    if len(parts) < 2:
        return []

    try:
        args = list(map(float, parts[1:]))
    except:
        return []

    func = parts[0]
    answer = None

    if func == 'min':
        answer = 'The minimum is: ' + str(min(args))
    elif func == 'max':
        answer = 'The Maximum is: ' + str(max(args))
    elif func == 'avg':
        answer = 'The Average is: ' + str(sum(args) / len(args))
    elif func == 'sum':
        answer = 'The sum is: ' + str(sum(args))
    elif func == 'prod':
        answer = 'The folded value is: ' + str(reduce(mul, args, 1))

    if answer is None:
        return []

    return [{'answer': str(answer)}]


# required answerer function
# returns information about the answerer
def self_info():
    return {'name': gettext('Statistics functions'),
            'description': gettext('Compute {functions} of the arguments').format(functions='/'.join(keywords)),
            'examples': ['avg 123 548 2.04 24.2']}
