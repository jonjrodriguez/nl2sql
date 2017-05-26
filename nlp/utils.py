import re
from nltk.corpus import wordnet
from nltk.metrics import jaccard_distance

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
    if word2 == "id":
        return 0

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
