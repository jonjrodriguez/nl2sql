import cPickle as pickle
from nltk.tokenize.stanford import StanfordTokenizer
from nltk.tag.stanford import StanfordNERTagger
from nltk.tag.hmm import HiddenMarkovModelTagger
from Config import Config

class Tagger(object):
    """
    Tag a sentence
    """
    def __init__(self):
        config = Config()

        jar_path = config.get("PATHS", "stanford_jar")
        stanford_models = config.get("PATHS", "stanford_models")
        ner_model_path = "%s/ner/english.conll.4class.distsim.crf.ser.gz" % stanford_models
        corpus_path = config.get("DATABASE", "corpus_path")

        self.tokenizer = StanfordTokenizer(jar_path)
        self.ner_tagger = StanfordNERTagger(ner_model_path, jar_path)

        corpus = pickle.load(open(corpus_path, "rb"))
        self.hmm_tagger = HiddenMarkovModelTagger.train(corpus)


    def tokenize(self, statement):
        return self.tokenizer.tokenize(statement)


    def ner(self, statement):
        tokens = self.tokenize(statement)
        return self.ner_tagger.tag(tokens)


    def tag_db_values(self, statement):
        tokens = self.tokenize(statement)
        return self.hmm_tagger.tag(tokens)
