from parse import Parser

class CorpusGenerator(object):
    """
    Methods to generate corpuses for later tagging and use
    """
    def __init__(self):
        self.parser = Parser()


    def create_db_corpus(self, database, path):
        tables = {
            'campuses': ['location'],
            'courses': ['peoplesoft_course_id', 'name'],
            'faculty_members': ['first_name', 'last_name'],
            'sections': ['name', 'peoplesoft_course_id', 'section_number'],
            'students': ['first_name', 'last_name', 'university_id', 'net_id', 'email'],
            'terms': ['semester', 'year']
        }

        with open(path, "wb") as corpus:
            for table in tables:
                cursor = database.execute("SELECT %s FROM %s" % (", ".join(tables[table]), table))
                rows = cursor.fetchall()
                for row in rows:
                    for i, value in enumerate(row):
                        if " " in str(value):
                            tokens = self.parser.tokenize(value)
                            for token in tokens:
                                corpus.write("%s\t%s.%s\n" % (token, table, tables[table][i]))
                        else:
                            corpus.write("%s\t%s.%s\n" % (value, table, tables[table][i]))
                    corpus.write("\n")
