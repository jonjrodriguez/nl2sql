from random import choice

CONTINUATIONS = [
    'Anything else?',
    'What else would you like to know?',
    'What else?'
]

def get_continuation():
    return choice(CONTINUATIONS)