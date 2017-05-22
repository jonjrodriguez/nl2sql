import re
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


    def choose(self, token, options):
        selected = 0

        # Constructing the message that will be displayed to the user
        choices = ['Which of these options best categorizes your use of the term ' + token + ' ?']
        for i in range(0, len(options)):
            term, _ = options[i]
            terms = re.split(r'\W+|_', term)
            formatted_terms = " ".join(terms)
            choices.append(str(i + 1) + ") " + formatted_terms.title())

        output = "\n".join(choices)
        output += "\n>"
        selected = self.ask(output)

        # Validation to make sure the user only enters a valid option
        while True:
            is_valid = selected.isdigit() and (int(selected) > 0) and (
                int(selected) <= len(options))

            if not is_valid:
                self.say("You have made an invalid entry. Please enter a number from 1 to %s" % len(options))
                selected = self.ask(output)
            else:
                break

        return int(selected) - 1
