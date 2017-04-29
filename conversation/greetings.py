from random import choice

GREETINGS = [
    'How can I help you?',
    'What can I do for you today?',
    'AMAA (Ask me almost anything):'
]

def get_greeting():
    return choice(GREETINGS)
