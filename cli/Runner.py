from Config import Config
from communicate import Communicator
from database import SchemaGraph
from nlp import DBCorpusClassifier, DBSchemaClassifier, Parser, Tagger, Tokenizer, NodeGenerator, Sanitizer

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

        #tagger = Tagger(paths['stanford_jar'], paths['stanford_models'])
        parser = Parser(paths['stanford_jar'], paths['stanford_models_jar'])
        corpus_classifier = DBCorpusClassifier(models['db_model'])
        schema_classifier = DBSchemaClassifier(schema_graph)
        sanitizer = Sanitizer()
        node_generator = NodeGenerator()

        self.pipeline = [sanitizer, parser, node_generator, corpus_classifier, schema_classifier]


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

            #for key, value in doc.iteritems():
            #    print "%s: " % key
            #    print value
            #    print

            self.communicator.resume()


    def make_doc(self, statement):
        return {
            'text': statement,
            'tokens': self.tokenizer(statement)
        }