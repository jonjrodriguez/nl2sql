"""
Command-line interface for NL2SQL
"""

import plac
from cli.download import download as cli_download
from cli.setup import setup as cli_setup
from cli.run import run as cli_run
from cli.test import main as cli_test

commands = 'download', 'setup', 'run', 'test'

@plac.annotations(
    path=("Path to download models and jar files (default: ./stanford)", "option", "p", str)
)
def download(path):
    """
    Download the Stanford CoreNLP tools and related models.
    Install the needed project dependencies.
    """
    cli_download(path or './stanford')

def setup():
    """
    Setup the project as needed.
    """
    cli_setup()

def run():
    """
    Start NL2SQL to parse questions
    """
    cli_run()

@plac.annotations(
    method=("Test method to run", "positional", None, str, ['tag', 'ner', 'parse'])
)
def test(method):
    """
    Scratch area to test different taggers and parsers
    """
    cli_test(method)

def __missing__(name):
    print("\n   Command %r does not exist."
          "\n   Use the --help flag for a list of available commands.\n" % name)

main = __import__(__name__)

if __name__ == '__main__':
    plac.call(main)
