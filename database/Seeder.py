from collections import OrderedDict
from random import choice
from faker import Faker

class Seeder(object):
    """
    Creates fake data to see database.
    """
    def __init__(self):
        self.fake = Faker()


    def get_seeds(self):
        seeds = OrderedDict()

        seeds['terms'] = self.create_terms()
        seeds['campuses'] = self.create_campuses()
        seeds['faculty'] = self.create_faculty()
        seeds['courses'] = self.create_courses(seeds['campuses'])
        seeds['sections'] = self.create_sections(seeds['courses'], seeds['terms'], seeds['campuses'], seeds['faculty'])
        seeds['students'] = self.create_students()
        seeds['registrations'] = self.create_registrations(seeds['students'], seeds['sections'])

        return seeds


    def create_terms(self):
        semesters = ['fall', 'spring', 'summer']

        terms = []
        for i in range(1, 10):
            terms.append({
                'id': i,
                'semester': choice(semesters),
                'year': self.fake.date_time_this_decade().year
            })

        return terms


    def create_campuses(self):
        campuses = []

        for i in range(1, 4):
            campuses.append({
                'id': i,
                'location': self.fake.state()
            })

        return campuses


    def create_faculty(self):
        faculty = []
        for i in range(1, 20):
            first_name = self.fake.first_name()
            last_name = self.fake.last_name()

            faculty.append({
                'id': i,
                'first_name': first_name,
                'last_name': last_name,
                'name': "%s %s" % (first_name, last_name),
                'is_adjunct': int(self.fake.boolean())
            })

        return faculty


    def create_courses(self, campuses):
        course_names = ['Graduate Lawyering I', 'Constitutional Law', 'Accounting For Lawyers',
                        'International Tax', 'Negotiation', 'Insurance Law', 'Evidence',
                        'International Law (for 1Ls)', 'Bankruptcy Tax', 'Copyright Law']

        courses = []
        for i in range(1, 11):
            courses.append({
                'id': i,
                'peoplesoft_course_id': 'LAW-LW.%d' % self.fake.random_number(digits=5, fix_len=True),
                'name': course_names[i-1],
                'active': int(self.fake.boolean())
            })

        return courses


    def create_sections(self, courses, terms, campuses, faculty):
        sections = []
        for i in range(1, 50):
            course = choice(courses)
            term = choice(terms)
            start_date = self.fake.date_time_this_decade()
            end_date = self.fake.date_time_between_dates(start_date)

            sections.append({
                'id': i,
                'course_id': course['id'],
                'term_id': term['id'],
                'campus_id': choice(campuses)['id'],
                'faculty_id': choice(faculty)['id'],
                'section_number': self.fake.random_int(1, 50),
                'active': int(self.fake.boolean()),
                'searchable': int(self.fake.boolean()),
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'credits': self.fake.random_int(0, 5),
                'max_enrollment': self.fake.random_int(20, 100),
                'description': self.fake.text()
            })

        return sections


    def create_students(self):
        students = []
        for i in range(1, 100):
            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            net_id = "%s%s%d" % (first_name[0].lower(), last_name[0].lower(), self.fake.random_number(digits=4))

            students.append({
                'id': i,
                'first_name': first_name,
                'last_name': last_name,
                'name': "%s %s" % (first_name, last_name),
                'university_id': 'N%d' % self.fake.random_number(digits=9, fix_len=True),
                'net_id': net_id,
                'active': int(self.fake.boolean()),
                'email': '%s@nyu.edu' % net_id,
            })

        return students


    def create_registrations(self, students, sections):

        registrations = []
        index = 1

        for student in students:
            for _ in range(self.fake.random_int(0, 6)):
                registrations.append({
                    'id': index,
                    'student_id': student['id'],
                    'section_id': choice(sections)['id']
                })

                index += 1

        return registrations
