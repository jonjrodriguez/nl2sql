from Config import Config
from nlp import CorpusClassifier, Parser, SimFinder, Tagger

class Runner(object):
    """
    Starts the NL2SQL system
    """
    def __init__(self, communicator):
        self.config = Config()
        db_model = self.config.get("MODELS", "db_model")

        self.comm = communicator

        self.classifier = CorpusClassifier(db_model)
        self.parser = Parser()
        self.tagger = Tagger()
        self.sim_finder = SimFinder()


    def start(self):
        self.comm.say("Type 'exit' to quit")

        self.comm.greet()
        self.start_loop()


    def start_loop(self):
        while True:
            statement = self.comm.ask(">")

            if statement.lower() == 'exit':
                break
            
            tokens = self.tagger.tokenize(statement)
            
            matches = self.sim_finder.find_db_matches(tokens)
            self.comm.say(matches)

            # parses = self.parser.parse(statement)
            # self.comm.say(parses)

            # tags = self.classifier.classify(tokens)
            # self.comm.say(tags)

            self.comm.resume()
