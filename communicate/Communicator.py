from random import choice
from communicate import phrases

class Communicator(object):
    """
    Communicates with the user.
    """
    def __init__(self):
        self.greetings = phrases.GREETINGS
        self.continuations = phrases.CONTINUATIONS
        self.answers = phrases.ANSWERS


    def greet(self):
        message = choice(self.greetings)
        self.say(message)


    def resume(self):
        message = choice(self.continuations)
        self.say(message)


    def say(self, message):
        print "\n   %s\n" % message


    def ask(self, message):
        return raw_input("   %s: " % message)


    def confirm(self, message):
        reply = None
        while reply not in self.answers:
            reply = self.ask("%s [y/n]" % message).lower()

        return self.answers[reply]


    def error(self, message):
        print "\n   %s\n" % message
        exit()
