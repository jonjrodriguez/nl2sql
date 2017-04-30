from collections import OrderedDict
from random import choice
from faker import Faker

FAKE = Faker()


def seed(cursor):
    seeds = OrderedDict()

    seeds['terms'] = create_terms()
    seeds['campuses'] = create_campuses()
    seeds['faculty_members'] = create_faculty_members()
    seeds['courses'] = create_courses(seeds['campuses'])
    seeds['sections'] = create_sections(seeds['courses'], seeds['terms'], seeds['campuses'],
                                        seeds['faculty_members'])
    seeds['students'] = create_students()
    seeds['registrations'] = create_registrations(seeds['students'], seeds['sections'])

    save_seeds(cursor, seeds)


def create_terms():
    print "   Creating terms"

    semesters = ['fall', 'spring', 'summer']

    terms = []
    for i in range(1, 10):
        terms.append({
            'id': i,
            'semester': choice(semesters),
            'year': FAKE.date_time_this_decade().year
        })

    return terms


def create_campuses():
    print "   Creating campuses"

    campuses = []

    for i in range(1, 4):
        campuses.append({
            'id': i,
            'location': FAKE.state()
        })

    return campuses


def create_faculty_members():
    print "   Creating faculty members"

    faculty = []
    for i in range(1, 20):
        faculty.append({
            'id': i,
            'first_name': FAKE.first_name(),
            'last_name': FAKE.last_name(),
            'is_adjunct': int(FAKE.boolean())
        })

    return faculty


def create_courses(campuses):
    print "   Creating courses"

    course_names = ['Graduate Lawyering I', 'Constitutional Law', 'Accounting For Lawyers',
                    'International Tax', 'Negotiation', 'Insurance Law', 'Evidence',
                    'International Law (for 1Ls)', 'Bankruptcy Tax', 'Copyright Law']

    courses = []
    for i in range(1, 11):
        courses.append({
            'id': i,
            'campus_id': choice(campuses)['id'],
            'peoplesoft_course_id': 'LAW-LW.%d' % FAKE.random_number(digits=5, fix_len=True),
            'name': course_names[i-1],
            'active': int(FAKE.boolean())
        })

    return courses


def create_sections(courses, terms, campuses, faculty):
    print "   Creating sections"

    sections = []
    for i in range(1, 50):
        course = choice(courses)
        term = choice(terms)
        start_date = FAKE.date_time_this_decade()
        end_date = FAKE.date_time_between_dates(start_date)

        sections.append({
            'id': i,
            'course_id': course['id'],
            'term_id': term['id'],
            'campus_id': choice(campuses)['id'],
            'faculty_member_id': choice(faculty)['id'],
            'peoplesoft_course_id': course['peoplesoft_course_id'],
            'section_number': FAKE.random_int(1, 50),
            'name': course['name'],
            'active': int(FAKE.boolean()),
            'searchable': int(FAKE.boolean()),
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'credits': FAKE.random_int(0, 5),
            'max_enrollment': FAKE.random_int(20, 100),
            'description': FAKE.text()
        })

    return sections


def create_students():
    print "   Creating students"

    students = []
    for i in range(1, 100):
        first_name = FAKE.first_name()
        last_name = FAKE.last_name()
        net_id = "%s%s%d" % (first_name[0].lower(), last_name[0].lower(),
                             FAKE.random_number(digits=4))

        students.append({
            'id': i,
            'first_name': first_name,
            'last_name': last_name,
            'university_id': 'N%d' % FAKE.random_number(digits=9, fix_len=True),
            'net_id': net_id,
            'active': int(FAKE.boolean()),
            'email': '%s@nyu.edu' % net_id,
        })

    return students


def create_registrations(students, sections):
    print "   Creating registrations"

    statuses = ['Enrolled', 'Dropped']

    registrations = []
    index = 1

    for student in students:
        for _ in range(FAKE.random_int(0, 6)):
            registrations.append({
                'id': index,
                'student_id': student['id'],
                'section_id': choice(sections)['id'],
                'status': choice(statuses)
            })

            index += 1

    return registrations


def save_seeds(cursor, seeds):
    print "\n   Saving seeds to database"

    for table_name, items in seeds.iteritems():
        statement = "INSERT INTO %s " % table_name
        statement += "(%s) VALUES " % ", ".join(items[0].keys())
        statement += "(%s)" % ", ".join(["%s" for _ in range(len(items[0].keys()))])

        cursor.executemany(statement, [tuple(item.values()) for item in items])
        