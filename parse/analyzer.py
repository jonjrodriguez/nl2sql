from settings import JAR_PATH, MODELS_JAR_PATH
from Parser import MyParser

def parse(statement):
    parser = MyParser(JAR_PATH, MODELS_JAR_PATH)
    parser.raw_parse(statement)
