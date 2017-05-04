from Config import Config
from nlp import Classifier, Parser, Tagger

class Runner(object):
    """
    Starts the NL2SQL system
    """
    def __init__(self, communicator):
        self.config = Config()
        db_model = self.config.get("MODELS", "db_model")

        self.comm = communicator

        self.tagger = Tagger()
        self.classifier = Classifier(db_model)
        self.parser = Parser()


    def start(self):
        self.comm.say("Type 'exit' to quit")

        self.comm.greet()
        self.start_loop()


    def start_loop(self):
        while True:
            statement = self.comm.ask(">")

            if statement.lower() == 'exit':
                break

            # parses = self.parser.parse(statement)
            # self.comm.say(parses)

            tokens = self.tagger.tokenize(statement)

            tags = self.classifier.classify(tokens)
            self.comm.say(tags)

            self.comm.resume()
