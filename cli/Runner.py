from nlp import Parser, SimFinder, Tagger

class Runner(object):
    """
    Starts the NL2SQL system
    """
    def __init__(self, communicator):
        self.comm = communicator

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
            
            # parses = self.parser.parse(statement)

            tokens = self.tagger.tokenize(statement)
            matches = self.sim_finder.find_db_matches(tokens)

            self.comm.say(matches)

            self.comm.resume()
