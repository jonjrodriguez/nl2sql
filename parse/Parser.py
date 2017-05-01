from nltk.tokenize.stanford import StanfordTokenizer
from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger
from nltk.parse.stanford import StanfordParser
from Config import Config

class Parser(object):
    """
    Parse and analyze sentence structure
    """
    def __init__(self):
        config = Config()

        jar_path = config.get("PATHS", "stanford_jar")
        stanford_models_jar = config.get("PATHS", "stanford_models_jar")
        stanford_models = config.get("PATHS", "stanford_models")

        pos_model_path = "%s/pos-tagger/english-left3words/english-left3words-distsim.tagger" % stanford_models
        ner_model_path = "%s/ner/english.conll.4class.distsim.crf.ser.gz" % stanford_models

        self.tokenizer = StanfordTokenizer(jar_path)

        self.pos_tagger = StanfordPOSTagger(pos_model_path, jar_path)
        self.ner_tagger = StanfordNERTagger(ner_model_path, jar_path)

        self.parser = StanfordParser(jar_path, stanford_models_jar)


    def tag(self, statement):
        tokens = self.tokenizer.tokenize(statement)
        return self.pos_tagger.tag(tokens)


    def ner(self, statement):
        tokens = self.tokenizer.tokenize(statement)
        return self.ner_tagger.tag(tokens)


    def parse(self, statement):
        return list(self.parser.raw_parse(statement))
