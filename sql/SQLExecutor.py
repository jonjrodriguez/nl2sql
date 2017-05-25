import mysql.connector
from mysql.connector import errorcode
from Config import Config


class SQLExecutor(object):
    def __init__(self, sql, comm):
        self.sql = sql
        self.config = Config()
        self.comm = comm

    def execute(self):
        # This should never happen but just to be safe
        if not self.config.has("DATABASE"):
            self.comm.say("Database has not been setup, please run setup to continue.")
            return

        config = {
            'user': str(self.config.get("DATABASE", "username")),
            'password': str(self.config.get("DATABASE", "password")),
            'host': str(self.config.get("DATABASE", "hostname")),
            'database': str(self.config.get("DATABASE", "database")),
            'raise_on_warnings': True,
        }

        try:
            cnx = mysql.connector.connect(**config)

            self.comm.say("Connecting to database")

            cursor = cnx.cursor(buffered=True)
            cursor.execute(self.sql)

            cnx.commit()

            columns = []
            tavnit = '|'
            separator = '+'

            results = cursor.fetchall()


            sizetable = [map(len, row) for row in results]
            widths = map(max, zip(*sizetable))

            for cd in cursor.description:
                columns.append(cd[0])

            for w in widths:
                tavnit += " %-" + "%ss |" % (w,)
                separator += '-' * w + '--+'

            print(separator)
            print(tavnit % tuple(columns))
            print(separator)
            for row in results:
                print(tavnit % row)
            print(separator)


        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cnx.close()
