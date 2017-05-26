import os
from warnings import filterwarnings, resetwarnings
import MySQLdb
from _mysql_exceptions import OperationalError
from database.Seeder import Seeder
from Config import Config

class Database(object):
    """
    Communicates with a MySQL database
    """
    def __init__(self, use_db_name=True):
        config = Config()
        db_settings = dict(config.items("DATABASE"))

        if db_settings:
            if not db_settings:
                raise ValueError('No database settings were found. Run setup to continue')

            if use_db_name:
                config = {
                    'host': db_settings["hostname"],
                    'user': db_settings["username"],
                    'passwd': db_settings["password"],
                    'db': db_settings["database"]
                }
            else:
                config = {
                    'host': db_settings["hostname"],
                    'user': db_settings["username"],
                    'passwd': db_settings["password"]
                }

        else:
            raise ValueError ("No database has been setup. Please run setup and try again.")

        try:
            self.database = MySQLdb.connect(**config)
        except OperationalError as (_, error):
            raise ValueError('Incorrect settings given for the database. %s' % error)


    def set_db(self, db_name):
        try:
            self.database.select_db(db_name)
            self.database.commit()
        except OperationalError as (_, error):
            raise ValueError('Incorrect name given for the database. %s' % error)


    def create_db(self, db_name):
        self.execute("CREATE DATABASE %s;" % db_name)
        self.database.select_db(db_name)


    def get_tables(self):
        cursor = self.execute("SHOW TABLES;")
        return cursor.fetchall()


    def get_fields(self, table):
        cursor = self.execute("DESCRIBE %s" % table)
        return cursor.fetchall()


    def get_foreign_keys(self):
        cursor = self.execute("SELECT DATABASE()")
        current_db = cursor.fetchone()[0]

        self.set_db("INFORMATION_SCHEMA")

        cursor = self.execute("""SELECT TABLE_NAME,COLUMN_NAME,CONSTRAINT_NAME,
            REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME from KEY_COLUMN_USAGE WHERE
            TABLE_SCHEMA = "%s" and referenced_column_name is not NULL;""" % current_db)

        foreign_keys = cursor.fetchall()

        self.set_db(current_db)

        return foreign_keys


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


    def execute(self, statement, show=False):
        cursor = self.database.cursor()
        cursor.execute(statement)

        if show:
            columns = []
            tavnit = '|'
            separator = '+'

            results = cursor.fetchall()
            sizetable = [map(len, map(str, row)) for row in results]
            widths = map(max, zip(*sizetable))

            for cd in cursor.description:
                columns.append(cd[0])

            columns_widths = []
            for cols_ls in columns:
                columns_widths.append(len(cols_ls))

            new_widths = []
            for i in range(0, len(widths)):
                new_widths.append(widths[i] + columns_widths[i])

            for w in new_widths:
                tavnit += " %-" + "%ss |" % (w,)
                separator += '-' * w + '--+'

            print(separator)
            print(tavnit % tuple(columns))
            print(separator)
            for row in results:
                print(tavnit % row)
            print(separator)

        return cursor

    def executemany(self, statement, values):
        cursor = self.database.cursor()
        cursor.executemany(statement, values)

    def does_db_exist(self, db_name):
        try:
            results = self.execute("SHOW DATABASES;")
            for result in results:
                print result

            if results:
                return True
            else:
                return False
        except MySQLdb.Error:
            print "ERROR IN CONNECTION"

        return False