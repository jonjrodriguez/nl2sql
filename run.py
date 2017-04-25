import argparse
import nltk

def tokenize(query):
    return nltk.word_tokenize(' '.join(query))

def tag(query):
    tokens = tokenize(query)

    tagged_tokens = nltk.pos_tag(tokens)

    print 'tagged:', tagged_tokens
    return tagged_tokens

def np_chunk(query):
    grammar = r"""
        NBAR: {<NN.*|JJ>*<NN.*>}

        NP: {<NBAR>}
            {<NBAR><IN><NBAR>}
    """

    chunker = nltk.RegexpParser(grammar)

    tagged_tokens = tag(query)
    chunked_tokens = chunker.parse(tagged_tokens)

    print 'np chunked:', chunked_tokens
    return chunked_tokens

def ne_chunk(query):
    tagged_tokens = tag(query)

    chunked_tokens = nltk.ne_chunk(tagged_tokens)

    print 'ne chunked:', chunked_tokens
    return chunked_tokens

def main():
    parser = argparse.ArgumentParser(description='Transform Natural Language to SQL')
    parser.add_argument('method', choices=['tag', 'np_chunk', 'ne_chunk'],
                        help='The functionality you wish to invoke')
    parser.add_argument('query', nargs='+', help='Your natural language query')

    args = parser.parse_args()

    switcher = {
        'tag': tag,
        'np_chunk': np_chunk,
        'ne_chunk': ne_chunk
    }

    func = switcher.get(args.method)
    func(args.query)

if __name__ == '__main__':
    main()
