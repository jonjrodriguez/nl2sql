from nltk.tokenize import word_tokenize
from nltk.classify.naivebayes import NaiveBayesClassifier
from utils.pickleHelper import load_pickle, save_pickle

# Should only be used to train a Naive Bayes Corpus were the
# Corpus has the following format:
# "Article", "Tag"

class Trainer(object):
    def __init__(self, data_file_path):
        self.data_path = data_file_path
        with open(self.data_path, "rb") as data_file:
            features = data_file.read().splitlines()

        self.feature_tuples = [feature.split("\t") for feature in features]
        self.word_set = self.get_words_from_features(self.feature_tuples)

        pass

    def train(self, model_path):
        train_set = [(self.featurize(feature), tag) for tag, feature in self.feature_tuples]

        classifier = NaiveBayesClassifier.train(train_set)
        save_pickle(classifier, model_path)
        return self

    def get_words_from_features(self, question_tuples):
        all_words = [word for _, question in question_tuples for word in word_tokenize(question)]

        return set(all_words)

    def featurize(self, question):
        tokens = word_tokenize(question)

        features = {'contains({0})'.format(word): (word in tokens) for word in self.word_set}
        return features
