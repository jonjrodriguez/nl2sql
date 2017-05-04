import cPickle as pickle
from nltk import MaxentClassifier
from nlp.utils import shape

class Classifier(object):
    """
    Classify statements based on trained models
    """
    def __init__(self, model_path=None):
        if model_path:
            with open(model_path, "rb") as model_file:
                self.classifier = pickle.load(model_file)


    def classify(self, statement):
        history = []
        for i, word in enumerate(statement):
            feature_set = self.db_row_features(statement, i, history)
            tag = self.classifier.classify(feature_set)
            history.append(tag)

        return zip(statement, history)


    def train_db_classifier(self, corpus_path, model_path):
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
