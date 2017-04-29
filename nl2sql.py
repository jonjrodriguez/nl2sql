"""
Command-line interface for NL2SQL
"""

import os
import plac
from cli.download import download as cli_download
from cli.setup import setup as cli_setup
from cli.run import run as cli_run
from cli.test import main as cli_test

commands = 'download', 'setup', 'run', 'test'

@plac.annotations(
    path=("Path to download models and jar files (default: ./data)", "option", "p", str),
    force=("Force download of all files", "flag", "f", bool)
)
def download(path, force):
    """
    Download the Stanford CoreNLP tools and related models.
    Install the needed project dependencies.
    """
    cli_download(path or './data', force)

def setup():
    """
    Setup the project as needed.
    """
    if not os.path.isfile('config.cfg'):
        print "\n   Make sure to run the download command first.\n"
        exit()

    cli_setup()

def run():
    """
    Start NL2SQL to parse questions
    """
    if not os.path.isfile('config.cfg'):
        print "\n   Make sure to run the download and setup commands first.\n"
        exit()

    cli_run()

@plac.annotations(
    method=("Test method to run", "positional", None, str, ['tag', 'ner', 'parse'])
)
def test(method):
    """
    Scratch area to test different taggers and parsers
    """
    if not os.path.isfile('config.cfg'):
        print "\n   Make sure to run the download command first.\n"
        exit()

    cli_test(method)

def __missing__(name):
    print("\n   Command %r does not exist."
          "\n   Use the --help flag for a list of available commands.\n" % name)

main = __import__(__name__)

if __name__ == '__main__':
    plac.call(main)
