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

        self.parser = StanfordParser(jar_path, stanford_models_jar)


    def parse(self, statement):
        return list(self.parser.raw_parse(statement))
