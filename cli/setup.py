from ConfigParser import ConfigParser
from database.utils import check_db, import_schema, seed_db


def setup():
    print "\n   Setting up NL2SQL.\n"

    config = ConfigParser()
    config.read('config.cfg')

    setup_database(config)

    with open('config.cfg', 'wb') as config_file:
        config.write(config_file)

    print "\n   Set up complete.\n"


def setup_database(config):
    if config.has_section('DATABASE'):
        print "\n   Database already configured."
        return

    print "\n   Configuring Database:\n"

    hostname = raw_input('   Enter hostname: ')
    username = raw_input('   Enter MySQL user: ')
    password = raw_input('   Enter MySQL password: ')
    database = raw_input('   Enter database name: ')

    try:
        check_db(hostname, username, password, database)
    except ValueError as exception:
        print "\n   Error: %s\n" % exception
        exit()

    if confirm("\n   Do you want to import the database schema?"):
        import_schema(hostname, username, password, database)

    if confirm("\n   Do you want to seed the database?"):
        seed_db(hostname, username, password, database)

    config.add_section('DATABASE')
    config.set('DATABASE', 'hostname', hostname)
    config.set('DATABASE', 'username', username)
    config.set('DATABASE', 'password', password)
    config.set('DATABASE', 'database', database)

    print "\n   Database configured.\n"


def confirm(message):
    answers = {'yes': True, 'y': True, 'no': False, 'n': False}

    reply = ''
    while reply not in answers:
        reply = raw_input("%s [y/n]: " % message).lower()

    return answers[reply]
