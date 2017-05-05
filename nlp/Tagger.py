from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger

class Tagger(object):
    """
    Tag sentence
    """
    def __init__(self, jar_path, model_path):
        pos_model_path = "%s/pos-tagger/english-left3words/english-left3words-distsim.tagger" % model_path
        ner_model_path = "%s/ner/english.conll.4class.distsim.crf.ser.gz" % model_path

        self.pos_tagger = StanfordPOSTagger(pos_model_path, jar_path)
        self.ner_tagger = StanfordNERTagger(ner_model_path, jar_path)
    

    def __call__(self, doc):
        doc['pos'] = self.tag(doc['tokens'])
        doc['ner'] = self.ner(doc['tokens'])


    def tag(self, tokens):
        return self.pos_tagger.tag(tokens)


    def ner(self, tokens):
        return self.ner_tagger.tag(tokens)
