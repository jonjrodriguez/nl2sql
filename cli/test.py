from nltk.tokenize.stanford import StanfordTokenizer
from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger
from nltk.parse.stanford import StanfordParser, StanfordDependencyParser
from settings import JAR_PATH, MODELS_JAR_PATH, POS_MODEL_PATH, NER_MODEL_PATH

def tag(query):
    tagger = StanfordPOSTagger(POS_MODEL_PATH, JAR_PATH)
    return tagger.tag(StanfordTokenizer(JAR_PATH).tokenize(query))

def ner(query):
    tagger = StanfordNERTagger(NER_MODEL_PATH, JAR_PATH)
    return tagger.tag(StanfordTokenizer(JAR_PATH).tokenize(query))

def parse(query):
    parser = StanfordParser(JAR_PATH, MODELS_JAR_PATH)
    result = parser.raw_parse(query)
    tree = result.next()

    print tree
    print tree.pretty_print()

    dep_parser = StanfordDependencyParser(JAR_PATH, MODELS_JAR_PATH)
    result = dep_parser.raw_parse(query)
    tree = result.next()

    print tree.tree()
    print tree.tree().pretty_print()
    return list(tree.triples())

def main(method):
    print "Type 'exit' to quit\n"

    methods = {
        'tag': tag,
        'ner': ner,
        'parse': parse
    }

    while True:
        input = raw_input("Enter a sentence:\n")

        if (input.lower() == 'exit'):
            break

        print methods[method](input)
