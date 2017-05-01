from Config import Config
from database import Database

class Setup(object):
    """
    Setup required items for NL2SQL
    """
    def __init__(self, communicator):
        self.config = Config()
        self.comm = communicator


    def run(self, force):
        self.comm.say("Setting up NL2SQL.")

        self.setup_db(force)

        self.config.write()
        self.comm.say("Set up complete.")


    def setup_db(self, force):
        if not force and self.config.has("DATABASE"):
            self.comm.say("Database already configured.")
            return

        self.comm.say("Configuring Database:")

        hostname = self.comm.ask("Enter hostname")
        username = self.comm.ask("Enter MySQL user")
        password = self.comm.ask("Enter MySQL password")
        db_name = self.comm.ask("Enter database name")

        try:
            database = Database(hostname, username, password)
        except ValueError as exception:
            self.comm.error("Error: %s" % exception)

        db_exists = False
        try:
            database.set_db(db_name)
            db_exists = True
        except ValueError as exception:
            if self.comm.confirm("Database does not exist. Create it?"):
                database.create_db(db_name)
                db_exists = True

        if db_exists:
            if self.comm.confirm("Do you want to import the database schema?"):
                database.import_schema()

            if self.comm.confirm("Do you want to seed the database?"):
                database.seed()

        self.config.set("DATABASE", "hostname", hostname)
        self.config.set("DATABASE", "username", username)
        self.config.set("DATABASE", "password", password)
        self.config.set("DATABASE", "database", db_name)

        self.comm.say("Database configured.")
