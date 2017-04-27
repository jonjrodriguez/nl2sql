import argparse
from nltk.tokenize.stanford import StanfordTokenizer
from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger
from nltk.parse.stanford import StanfordParser, StanfordDependencyParser

PATH_TO_JAR = "./stanford/stanford-corenlp-3.7.0.jar"
PATH_TO_MODELS_JAR = "./stanford/stanford-corenlp-3.7.0-models.jar"

def tag(query):
    tagger = StanfordPOSTagger('./stanford/models/pos/english-bidirectional-distsim.tagger',
                               PATH_TO_JAR)

    return tagger.tag(StanfordTokenizer(PATH_TO_JAR).tokenize(query))

def ner(query):
    tagger = StanfordNERTagger('./stanford/models/ner/english.all.3class.distsim.crf.ser.gz',
                               PATH_TO_JAR)

    return tagger.tag(StanfordTokenizer(PATH_TO_JAR).tokenize(query))

def parse(query):
    parser = StanfordParser(PATH_TO_JAR, PATH_TO_MODELS_JAR)
    result = parser.raw_parse(query)
    tree = result.next()

    print tree
    print tree.pretty_print()

    dep_parser = StanfordDependencyParser(PATH_TO_JAR, PATH_TO_MODELS_JAR)
    result = dep_parser.raw_parse(query)
    tree = result.next()

    print tree.tree()
    print tree.tree().pretty_print()
    return list(tree.triples())

def main():
    parser = argparse.ArgumentParser(description='Transform Natural Language to SQL')
    parser.add_argument('method', choices=['tag', 'ner', 'parse'],
                        help='The functionality you wish to invoke')
    parser.add_argument('query', nargs='+', help='Your natural language query')

    args = parser.parse_args()

    switcher = {
        'tag': tag,
        'ner': ner,
        'parse': parse
    }

    func = switcher.get(args.method)
    result = func(' '.join(args.query))
    print result

if __name__ == '__main__':
    main()
