from Config import Config
from communicate import Communicator
from database import SchemaGraph
from nlp import DBCorpusClassifier, DBSchemaClassifier, SQLGrammarClassifier, Parser, Tokenizer

class Runner(object):
    """
    Starts the NL2SQL system. Creates the pipeline
    """
    def __init__(self):
        config = Config()
        paths = dict(config.items("PATHS"))
        db_settings = dict(config.items("DATABASE"))
        models = dict(config.items("MODELS"))

        self.communicator = Communicator()
        schema_graph = SchemaGraph(db_settings['graph_path'])

        self.tokenizer = Tokenizer(paths['stanford_jar'])

        parser = Parser(paths['stanford_jar'], paths['stanford_models_jar'])
        grammar_classifier = SQLGrammarClassifier(models['sql_model'])
        corpus_classifier = DBCorpusClassifier(models['db_model'])
        schema_classifier = DBSchemaClassifier(schema_graph)

        self.pipeline = [parser, grammar_classifier, schema_classifier, corpus_classifier]


    def start(self):
        self.communicator.say("Type 'exit' to quit")

        self.communicator.greet()
        self.start_loop()


    def start_loop(self):
        while True:
            statement = self.communicator.ask(">")

            if statement.lower() == 'exit':
                break

            doc = self.make_doc(statement)

            for process in self.pipeline:
                process(doc)

            for key, value in doc['tagged'].iteritems():
                print key, value

            print
            print doc['dep_parse'].tree().pretty_print()

            self.communicator.resume()


    def make_doc(self, statement):
        return {
            'text': statement,
            'tokens': self.tokenizer(statement),
            'tagged': {}
        }
