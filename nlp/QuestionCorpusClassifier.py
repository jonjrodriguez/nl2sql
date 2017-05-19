from Config import Config
from nlp.utils import load_pickle, save_pickle
from nltk.classify.naivebayes import NaiveBayesClassifier
from nltk.tokenize import word_tokenize


class QuestionCorpusClassifier(object):
    def __init__(self, model_path=None):
        config = Config()
        self.questions_corpus_path = config.get("QUESTIONS", "corpus_path")

        if model_path:
            self.classifier = load_pickle(model_path)

        with open(self.questions_corpus_path, "rb") as data_file:
            features = data_file.read().splitlines()

        self.feature_tuples = [feature.split("\t") for feature in features]
        self.word_set = self.get_words_from_features(self.feature_tuples)

    def __call__(self, doc):
        doc['question_corpus'] = self.classify(doc['text'])


    def classify(self, sentence):
        features = self.featurize(sentence)
        return self.classifier.classify(features)

    def train(self, model_path):
        train_set = [(self.featurize(feature), tag) for tag, feature in self.feature_tuples]

        self.classifier = NaiveBayesClassifier.train(train_set)
        save_pickle(self.classifier, model_path)

    def get_words_from_features(self, question_tuples):
        all_words = [word for _, question in question_tuples for word in word_tokenize(question)]

        return set(all_words)

    def featurize(self, question):
        tokens = word_tokenize(question)

        features = {'contains({0})'.format(word): (word in tokens) for word in self.word_set}
        return features
