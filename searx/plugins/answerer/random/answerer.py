import hashlib
import random
import string
import uuid
from flask_babel import gettext

# required answerer attribute
# specifies which search query keywords triggers this answerer
keywords = ('random',)

random_int_max = 2 ** 31
random_string_letters = string.ascii_lowercase + string.digits + string.ascii_uppercase

author = [{
    'name': 'Searx Core',
    'url': "https://github.com/searx/searx"
},{
    'name': 'Justin Back',
    'url': "https://github.com/JustinBack"
}]


def random_characters():
    return [random.choice(random_string_letters)
            for _ in range(random.randint(8, 32))]


def random_string():
    return ''.join(random_characters())


def random_float():
    return str(random.random())


def random_mac():
    _valid_char = "0123456789ABCDEF"
    _valid_bcast_char = "02468ACE"

    def _gen_rand_bytes(bytes_needed):
        out_bytes = []
        for i in range(bytes_needed):
            rand_byte = random.choice(_valid_char) + random.choice(_valid_char)
            out_bytes.append(rand_byte)
        out_bytes = ":".join(out_bytes)
        return out_bytes

    first_byte = random.choice(_valid_char) + random.choice(_valid_bcast_char)

    five_bytes = _gen_rand_bytes(5)
    out_mac = first_byte + ":" + five_bytes
    return str(out_mac)


def random_int():
    return str(random.randint(-random_int_max, random_int_max))


def random_sha256():
    m = hashlib.sha256()
    m.update(''.join(random_characters()).encode())
    return str(m.hexdigest())


def random_uuid():
    return str(uuid.uuid4())


random_types = {'string': random_string,
                'int': random_int,
                'integer': random_int,
                'float': random_float,
                'sha256': random_sha256,
                'mac': random_mac,
                'mac address': random_mac,
                'uuid': random_uuid}


def answer(query):
    parts = query.split()
    if len(parts) < 2:
        return []


    if parts[1] not in random_types:
        return []

    return {
        'answer': random_types[parts[1]]()
    }


def self_info():
    return {'name': gettext('Random value generator'),
            'description': gettext('Generate different random values'),
            'examples': ['random {}'.format(x) for x in random_types],
            'repository': '{repository}/src/{commit}/searx/plugins/answerer/random/answerer.py',
            'website': 'https://tosdr.org'}
