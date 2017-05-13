import re
from nltk.corpus import wordnet
from nltk.metrics import jaccard_distance
try:
    import cPickle as pickle
except:
    import pickle

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


def wup_sim(word1, word2):
    synset1 = wordnet.synsets(word1)
    synset2 = wordnet.synsets(word2)

    if not synset1 or not synset2:
        return 0

    if synset1[0] == synset2[0]:
        return 1.0

    return wordnet.wup_similarity(synset1[0], synset2[0])


def jaccard_sim(word1, word2):
    set1 = set(word1)
    set2 = set(word2)

    coefficient = 1 - jaccard_distance(set1, set2)

    return coefficient


def load_pickle(path):
    f = open(path, 'rb')
    result = pickle.load(f)
    f.close()
    return result


def save_pickle(data, path):
    with open(path, "wb") as data_file:
        pickle.dump(data, data_file)

COUNT_TYPE  = r'(how many|count of|number of)'
OPERATOR_EQUALITY_TYPE  = r'(equals)'
OPERATOR_INVERT_TYPE  = r'(not)'
OPERATOR_MANY_TYPE = r'((in|are|have|will|)(\s)(taking|taken|took|take))'
OPERATOR_MAX_TYPE = r'(most|greatest|best|largest|max)'
OPERATOR_MIN_TYPE = r'(least|smallest|worst|min)'
OPERATOR_GREATER_TYPE = r'((greater|bigger|more)\s(than|then))'
OPERATOR_LESS_TYPE = r'((less|fewer)(\s)(than|then))'
LIST_TYPE   = r'((list|give me)(\s)(several|all|a few|few|one|two|three|four|five|six|seven|eight|nine|ten))'
TIME_TYPE  = r'((1[012]|[1-9]):[0-5][0-9](\s)?(?i)(\s)*(am|pm))'
DATE_TYPE  = r'((0?[1-9]|1[012])/(0?[1-9]|[12][0-9]|3[01])/((19|20)\d\d))'
STOP_TYPE = r'((return|are there|)([.?]))'


ALL_TYPES = {
    'COUNT': COUNT_TYPE,
    'LIST': LIST_TYPE,
    'TIME': TIME_TYPE,
    'DATE': DATE_TYPE,
    'STOP': STOP_TYPE,
    'EQUALS': OPERATOR_EQUALITY_TYPE,
    'ONOT': OPERATOR_INVERT_TYPE,
    'OIN': OPERATOR_MANY_TYPE,
    'OMAX': OPERATOR_MAX_TYPE,
    'OMIN': OPERATOR_MIN_TYPE,
    'OLESS': OPERATOR_GREATER_TYPE,
    'OMORE': OPERATOR_LESS_TYPE
}