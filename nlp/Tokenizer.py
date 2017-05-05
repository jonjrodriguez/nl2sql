from nltk.tokenize.stanford import StanfordTokenizer

class Tokenizer(object):
    """
    Tokenize sentence
    """
    def __init__(self, jar_path):
        self.tokenizer = StanfordTokenizer(jar_path)


    def tokenize(self, sentence):
        return self.tokenizer.tokenize(sentence)


    def __call__(self, sentence):
        return self.tokenize(sentence)
