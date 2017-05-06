from Config import Config
from utils.pickleHelper import load_pickle
from Trainer import Trainer
from nltk.tokenize import word_tokenize


class QuestionClassifier:
    def __init__(self, load_previous_classifier=True):
        config = Config()
        self.questions_corpus = config.get("QUESTION_CLF", "corpus")
        self.questions_model_path = config.get("QUESTION_CLF", "cached_corpus")

        if load_previous_classifier:
            self.classifier = load_pickle(self.questions_model_path)

        self.trainer = Trainer(self.questions_corpus)

    def classify(self, question):
        features = self.trainer.featurize(question)
        return self.classifier.classify(features)

    def train(self):
        self.trainer = self.trainer.train(self.questions_model_path)