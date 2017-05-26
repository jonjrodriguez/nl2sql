"""
Command-line interface for NL2SQL
"""

import os
import plac
from communicate import Communicator
from cli import Download, Setup, Runner

commands = 'download', 'setup', 'run'


@plac.annotations(
    path=("Path to download models and jar files (default: ./data)", "option", "p", str),
    force=("Force download of all files", "flag", "f", bool)
)
def download(path, force):
    """
    Download the Stanford CoreNLP tools and related models.
    Install the needed project dependencies.
    """
    comm = Communicator()

    Download(comm, path or './data').run(force)


@plac.annotations(
    force=("Force setup to rerun", "flag", "f", bool)
)
def setup(force):
    """
    Setup the project as needed.
    """
    comm = Communicator()

    if not os.path.isfile('config.cfg'):
        comm.error('Make sure to run the download command first.')

    Setup(comm).run(force)

@plac.annotations(
    debug=("Print out debug statements", "flag", "d", bool)
)
def run(debug):
    """
    Start NL2SQL to parse questions
    """
    comm = Communicator()

    if not os.path.isfile('config.cfg'):
        comm.error('Make sure to run the download and setup commands first.')

    Runner().start(debug)


def __missing__(name):
    print("\n   Command %r does not exist."
          "\n   Use the --help flag for a list of available commands.\n" % name)

main = __import__(__name__)

if __name__ == '__main__':
    plac.call(main)
