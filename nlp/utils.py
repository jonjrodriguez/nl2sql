import re

def shape(word):
    if re.match(r'@', word, re.UNICODE):
        return 'email'

    if re.match(r'[0-9]+(\.[0-9]*)?|[0-9]*\.[0-9]+$', word, re.UNICODE):
        return 'number'

    if re.match(r'\W+$', word, re.UNICODE):
        return 'punct'

    if re.match(r'[a-zA-Z]+$', word, re.UNICODE):
        return 'alpha'

    if re.match(r'\w+$', word, re.UNICODE):
        return 'mixedchar'

    return 'other'
