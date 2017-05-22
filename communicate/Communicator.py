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

    def refineResult(self, token, nodeTag):
        selected_term = 0

        # Constructing the message that will be displayed to the user
        options = ['Which of these options best categorizes your use of the term ' + token + ' ?']
        for i in range(0, len(nodeTag)):
            term, score = nodeTag[i]
            terms = term.split(".")
            formatted_terms = " ".join(terms)
            options.append(str(i + 1) + ") " + formatted_terms.capitalize())

        output = "\n".join(options)
        output += "\n>"
        selected_term = self.ask(output)

        # Validation to make sure the user only enters a valid option
        while True:
            isValidInput = selected_term.isdigit() and (int(selected_term) > 0) and (
                int(selected_term) <= len(nodeTag))

            if not isValidInput:
                self.say("You have made an invalid entry. Please enter a number from 1 to " + str(len(nodeTag)))
                selected_term = self.ask(output)
            else:
                break

        return int(selected_term) - 1
