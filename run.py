import argparse
import nltk
from nltk.corpus import conll2000
from Chunkers import UnigramChunker, BigramChunker, MaxentChunker

def tokenize(query):
    return nltk.word_tokenize(' '.join(query))

def tag(query):
    tokens = tokenize(query)

    tagged_tokens = nltk.pos_tag(tokens)

    return tagged_tokens

def np_chunk(query):
    test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
    train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])

    unichunker = UnigramChunker.UnigramChunker(train_sents)
    bichunker = BigramChunker.BigramChunker(train_sents)
    # too slow
    # maxchunker = MaxentChunker.MaxentChunker(train_sents)

    print unichunker.evaluate(test_sents)
    print bichunker.evaluate(test_sents)
    # print maxchunker.evaluate(test_sents)

    tagged_tokens = tag(query)

    chunked_tokens2 = unichunker.parse(tagged_tokens)
    chunked_tokens3 = bichunker.parse(tagged_tokens)
    # chunked_tokens4 = maxchunker.parse(tagged_tokens)

    print 'np chunked:', chunked_tokens2
    print 'np chunked:', chunked_tokens3
    # print 'np chunked:', chunked_tokens4

    return chunked_tokens3

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
