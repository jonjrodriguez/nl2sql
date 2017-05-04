from nltk.tokenize.stanford import StanfordTokenizer
from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger
from Config import Config

class Tagger(object):
    """
    Tokenize and tag sentence
    """
    def __init__(self):
        config = Config()

        jar_path = config.get("PATHS", "stanford_jar")
        stanford_models = config.get("PATHS", "stanford_models")

        pos_model_path = "%s/pos-tagger/english-left3words/english-left3words-distsim.tagger" % stanford_models
        ner_model_path = "%s/ner/english.conll.4class.distsim.crf.ser.gz" % stanford_models

        self.tokenizer = StanfordTokenizer(jar_path)

        self.pos_tagger = StanfordPOSTagger(pos_model_path, jar_path)
        self.ner_tagger = StanfordNERTagger(ner_model_path, jar_path)


    def tokenize(self, statement):
        return self.tokenizer.tokenize(statement)


    def tag(self, statement):
        tokens = self.tokenize(statement)
        return self.pos_tagger.tag(tokens)


    def ner(self, statement):
        tokens = self.tokenize(statement)
        return self.ner_tagger.tag(tokens)
