import os
from warnings import filterwarnings, resetwarnings
import MySQLdb
from _mysql_exceptions import OperationalError, Warning
from database.seed import seed

DATABASE = None

def connect(host, user, passwd, db_name=''):
    global DATABASE
    DATABASE = MySQLdb.connect(host, user, passwd, db_name)


def get_database(host, user, passwd, db_name=None):
    if DATABASE is None:
        connect(host, user, passwd)

    if db_name:
        DATABASE.select_db(db_name)

    return DATABASE


def check_db(host, user ,passwd, database):
    try:
        connect(host, user, passwd, database)
    except OperationalError as (code, error):
        if code == 1049:
            print "\n   Database %s does not exist. Creating now" % database
            create_db(host, user, passwd, database)
            return

        raise ValueError('Incorrect settings given for the database. %s' % error)


def create_db(host, user, passwd, database):
    db = get_database(host, user, passwd)
    cur = db.cursor()

    cur.execute("CREATE DATABASE %s;" % database)


def import_schema(host, user, passwd, database):
    print "\n   Importing Database schema.\n"

    filterwarnings('ignore', category=Warning)

    db = get_database(host, user, passwd, database)
    cur = db.cursor()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, 'schema.sql')

    statement = ""
    for line in open(file_path).read().splitlines():
        if line.strip().startswith('--'):
            continue

        if not line.strip().endswith(';'):
            statement += line.strip()
            continue

        statement += line.strip()
        cur.execute(statement)

        statement = ""

    resetwarnings()

    print "\n   Database schema import complete.\n"


def seed_db(host, user, passwd, database):
    print "\n   Seeding Database with data.\n"

    db = get_database(host, user, passwd, database)
    cur = db.cursor()

    seed(cur)

    db.commit()

    print "\n   Finished Seeding Database.\n"
