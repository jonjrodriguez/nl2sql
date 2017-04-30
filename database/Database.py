import os
from warnings import filterwarnings, resetwarnings
import MySQLdb
from _mysql_exceptions import OperationalError
from database.Seeder import Seeder

class Database(object):
    """
    Communicates with a MySQL database
    """
    def __init__(self, host, user, passwd, db_name=''):
        try:
            self.database = MySQLdb.connect(host, user, passwd, db_name)
        except OperationalError as (_, error):
            raise ValueError('Incorrect settings given for the database. %s' % error)


    def set_db(self, db_name):
        try:
            self.database.select_db(db_name)
        except OperationalError as (_, error):
            raise ValueError('Incorrect name given for the database. %s' % error)


    def create_db(self, db_name):
        self.execute("CREATE DATABASE %s;" % db_name)
        self.database.select_db(db_name)


    def import_schema(self):
        filterwarnings('ignore', category=Warning)

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
            self.execute(statement)

            statement = ""

        resetwarnings()


    def seed(self):
        seeds = Seeder().get_seeds()

        for table_name, items in seeds.iteritems():
            statement = "INSERT INTO %s " % table_name
            statement += "(%s) VALUES " % ", ".join(items[0].keys())
            statement += "(%s)" % ", ".join(["%s" for _ in range(len(items[0].keys()))])

            self.executemany(statement, [tuple(item.values()) for item in items])

        self.database.commit()


    def execute(self, statement):
        cursor = self.database.cursor()
        cursor.execute(statement)


    def executemany(self, statement, values):
        cursor = self.database.cursor()
        cursor.executemany(statement, values)
