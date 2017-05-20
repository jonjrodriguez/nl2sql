import re
import cPickle as pickle
from nltk import MaxentClassifier
from nlp.utils import shape

class DBCorpusClassifier(object):
    """
    Classify tokens based on values in the database
    """
    def __init__(self, model_path=None):
        if model_path:
            with open(model_path, "rb") as model_file:
                self.classifier = pickle.load(model_file)


    def __call__(self, doc):
        trees = [tree.leaves() for tree in doc['parse'].subtrees(self.filter_tree)]
        tokens = [token for leaves in trees for token in leaves if token not in doc['tagged']]

        tags = self.classify(tokens)
        
        for tag in tags:
            doc['tagged'][tag[0]] = {
                'type': 'corpus',
                'tags': tag[1]
            }


    @staticmethod
    def filter_tree(tree):
        """
        Filters parse tree to certain POS in Noun Phrases
        May need to expand or remove this filter
        """
        if tree.parent() is None:
            return False

        noun_phrase = re.match("NP", tree.parent().label())
        pos = re.match("NN.*|JJ|CD", tree.label())

        return noun_phrase and pos


    def classify(self, tokens, limit=3):
        history = []
        results = []

        for i, _ in enumerate(tokens):
            feature_set = self.db_row_features(tokens, i, history)

            pdist = self.classifier.prob_classify(feature_set)
            labels = sorted(pdist.samples(), key=pdist.prob, reverse=True)

            history.append(pdist.max())
            results.append([(label, pdist.prob(label)) for label in labels[:limit]])

        return zip(tokens, results)


    def train(self, corpus_path, model_path):
        with open(corpus_path) as corpus_file:
            corpus = pickle.load(corpus_file)

        train_set = []
        for row in corpus:
            sentence = [value for (value, _) in row]
            history = []
            for i, (value, column) in enumerate(row):
                feature_set = self.db_row_features(sentence, i, history)
                train_set.append((feature_set, column))
                history.append(column)

        classifier = MaxentClassifier.train(train_set, max_iter=20)

        with open(model_path, "wb") as model_file:
            pickle.dump(classifier, model_file)


    def db_row_features(self, sentence, i, history):
        word = str(sentence[i])
        word_shape = shape(word)

        features = {
            'token': word,
            'lower': word.lower(),
            'shape': word_shape,
            'semester': word.lower() in ['summer', 'fall', 'winter', 'spring']
        }

        if i > 0:
            prev_token = str(sentence[i-1])
            features['prev_tag'] = history[i-1]
            features['prev_token'] = prev_token
            features['prev_lower'] = prev_token.lower()
            features['prev_token+token'] = "%s+%s" % (prev_token, word)
            features['prev_lower+lower'] = "%s+%s" % (prev_token.lower(), word.lower())
            features['prev_tag+token'] = "%s+%s" % (history[i-1], word)
            features['prev_tag+lower'] = "%s+%s" % (history[i-1], word.lower())
            features['prev_tag+shape'] = "%s+%s" % (history[i-1], word_shape)

        if i < len(sentence) - 1:
            next_token = str(sentence[i+1])
            features['next_token'] = next_token
            features['next_lower'] = next_token.lower()
            features['token+next_token'] = "%s+%s" % (word, next_token)
            features['lower+next_lower'] = "%s+%s" % (word.lower(), next_token.lower())

        return features
