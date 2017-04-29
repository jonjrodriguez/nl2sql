from parse import determineNegativeSentiment, parse
from conversation import get_greeting, get_continuation

def run():
    print "Type 'exit' to quit\n"

    i = 0
    while True:
        message = get_greeting() if i == 0 else get_continuation()
        input_statement = raw_input(message + "\n")
        
        if (determineNegativeSentiment(input_statement) == 1.0
            or input_statement.lower() == 'exit'):
            break

        parse(input_statement)
        
        i += 1
