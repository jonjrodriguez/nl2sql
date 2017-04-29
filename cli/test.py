from ConfigParser import ConfigParser
from nltk.tokenize.stanford import StanfordTokenizer
from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger
from nltk.parse.stanford import StanfordParser, StanfordDependencyParser


def tag(query, config):
    jar_path = config.get('PATHS', 'stanford_jar')
    models_path = config.get('PATHS', 'stanford_models')

    pos_model_path = ("%s/pos-tagger/english-left3words/english-left3words-distsim.tagger"
                      % models_path)

    tagger = StanfordPOSTagger(pos_model_path, jar_path)

    return tagger.tag(StanfordTokenizer(jar_path).tokenize(query))


def ner(query, config):
    jar_path = config.get('PATHS', 'stanford_jar')
    models_path = config.get('PATHS', 'stanford_models')

    ner_model_path = "%s/ner/english.conll.4class.distsim.crf.ser.gz" % models_path

    tagger = StanfordNERTagger(ner_model_path, jar_path)

    return tagger.tag(StanfordTokenizer(jar_path).tokenize(query))


def parse(query, config):
    jar_path = config.get('PATHS', 'stanford_jar')
    models_jar_path = config.get('PATHS', 'models_jar')

    parser = StanfordParser(jar_path, models_jar_path)
    result = parser.raw_parse(query)
    tree = result.next()

    print tree
    print tree.pretty_print()

    dep_parser = StanfordDependencyParser(jar_path, models_jar_path)
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

    config = ConfigParser()
    config.read('config.cfg')

    while True:
        sentence = raw_input("Enter a sentence:\n")

        if sentence.lower() == 'exit':
            break

        print methods[method](sentence, config)
