from Config import Config
from communicate import Communicator
from database import SchemaGraph, Database
from nlp import DBCorpusClassifier, DBSchemaClassifier, SQLGrammarClassifier, Parser, Tokenizer
from sql import NodeGenerator, SQLGenerator

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
        self.schema_graph = SchemaGraph(db_settings['graph_path'])

        self.tokenizer = Tokenizer(paths['stanford_jar'])

        parser = Parser(paths['stanford_jar'], paths['stanford_models_jar'])
        grammar_classifier = SQLGrammarClassifier(models['sql_model'])
        corpus_classifier = DBCorpusClassifier(models['db_model'])
        schema_classifier = DBSchemaClassifier(self.schema_graph)

        self.pipeline = [parser, grammar_classifier, schema_classifier, corpus_classifier]
        self.node_generator = NodeGenerator(self.communicator)


    def start(self, debug=False):
        self.communicator.say("Type 'exit' to quit")

        self.communicator.greet()
        self.start_loop(debug)


    def start_loop(self, debug):
        while True:
            statement = self.communicator.ask(">")

            if statement.lower() == 'exit':
                break

            doc = self.make_doc(statement)

            for process in self.pipeline:
                process(doc)

            tree = self.node_generator(doc)

            sql_generator = SQLGenerator(tree, self.schema_graph)
            sql = sql_generator.get_sql()

            if debug:
                self.print_debug(doc, tree, sql)

            database = Database()
            database.execute(sql, True)

            self.communicator.resume()


    def make_doc(self, statement):
        return {
            'text': statement,
            'tokens': self.tokenizer(statement),
            'tagged': {}
        }


    def print_debug(self, doc, tree, sql):
        self.communicator.say("Parse Pretty Print")
        doc['parse'].pretty_print()

        self.communicator.say("Dependency Parse Pretty Print")
        doc['dep_parse'].tree().pretty_print()

        self.communicator.say("Tagged tokens")
        for token, tags in doc['tagged'].items():
            print "   %s: %s" % (token, tags)

        self.communicator.say("SQL Tree Pretty Print")
        tree.pretty_print()

        self.communicator.say("SQL: %s" % sql)
