from nlp import Parser

class Runner(object):
    """
    Starts the NL2SQL system
    """
    def __init__(self, communicator):
        self.comm = communicator
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

            parses = self.parser.parse(statement)

            self.comm.say(parses)

            self.comm.resume()
