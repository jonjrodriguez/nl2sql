from ConfigParser import ConfigParser
from parse.Parser import MyParser


def parse(statement):
    config = ConfigParser()
    config.read('config.cfg')

    jar_path = config.get('PATHS', 'stanford_jar')
    models_jar_path = config.get('PATHS', 'models_jar')

    parser = MyParser(jar_path, models_jar_path)
    parser.raw_parse(statement)
