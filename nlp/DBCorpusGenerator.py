import cPickle as pickle
from nlp import Tagger

class DBCorpusGenerator(object):
    """
    Generate a corpus based on the database
    """
    def __init__(self):
        self.tagger = Tagger()


    def create_db_corpus(self, database, path):
        tables = {
            'campuses': ['location'],
            'courses': ['peoplesoft_course_id', 'name'],
            'faculty_members': ['first_name', 'last_name'],
            'sections': ['name', 'peoplesoft_course_id', 'section_number'],
            'students': ['first_name', 'last_name', 'university_id', 'net_id', 'email'],
            'terms': ['semester', 'year']
        }

        corpus = []
        for table in tables:
            cursor = database.execute("SELECT %s FROM %s" % (", ".join(tables[table]), table))
            rows = cursor.fetchall()
            for row in rows:
                sentence = []
                for i, value in enumerate(row):
                    label = "%s.%s" % (table, tables[table][i])
                    if " " in str(value):
                        tokens = self.tagger.tokenize(value)
                        for token in tokens:
                            sentence.append((token, label))
                    else:
                        sentence.append((value, label))

                corpus.append(sentence)

        pickle.dump(corpus, open(path, "wb"))
