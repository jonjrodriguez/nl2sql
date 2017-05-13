from nltk.parse.stanford import StanfordParser, StanfordDependencyParser

class Parser(object):
    """
    Parse sentence structure
    """
    def __init__(self, jar_path, model_path):
        self.parser = StanfordParser(jar_path, model_path)
        self.dep_parser = StanfordDependencyParser(jar_path, model_path)


    def __call__(self, doc):
        doc['parse'] = self.parse(doc['sanitized_text'])
        doc['dep_parse'] = self.dep_parse(doc['sanitized_text'])


    def parse(self, statement):
        return next(self.parser.raw_parse(statement))


    def dep_parse(self, statement):
        return next(self.dep_parser.raw_parse(statement))
