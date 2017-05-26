import cPickle as pickle
from nltk import BigramTagger, UnigramTagger, DefaultTagger
from nlp.SQLGrammarCorpus import CORPUS

class SQLGrammarClassifier(object):
    def __init__(self, model_path=None):
        if model_path:
            with open(model_path, "rb") as model_file:
                self.tagger = pickle.load(model_file)


    def __call__(self, doc):
        tokens = [token.lower() for token in doc['tokens'] if token not in doc['tagged']]

        tags = self.classify(tokens)

        for index, token in enumerate(doc['tokens']):
            if tags[index][1] == 'UNK':
                continue

            doc['tagged'][doc['tokens'][index]] = {
                'type': 'grammar',
                'tags': tags[index][1]
            }


    def classify(self, tokens):
        return self.tagger.tag(tokens)


    def train(self, model_path):
        corpus = [[(token.lower(), tag) for token, tag in sent] for sent in CORPUS]

        unigram_tagger = UnigramTagger(corpus, backoff=DefaultTagger('UNK'))
        bigram_tagger = BigramTagger(corpus, backoff=unigram_tagger)

        with open(model_path, "wb") as model_file:
            pickle.dump(bigram_tagger, model_file)
