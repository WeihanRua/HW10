import os
import sqlite3
from prettytable import PrettyTable
from collections import defaultdict


class Student():

    def __init__(self, cwid, name, major):

        self.cwid = cwid
        self.name = name
        self.major = major
        self.taken_courses = defaultdict(str)  # the key is the course code, the value is course grade
        self.pass_courses = set()
        self.remaining_required = set()    # copy from class major
        self.remaining_elective = set()    # copy from class major

    def add_course(self, course_code, grade):

        self.taken_courses[course_code] = grade

        if grade in ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']:   # judge if the course is pass

            self.pass_courses.add(course_code)
            self.remaining_required = self.remaining_required.difference(self.pass_courses)

            if len(self.remaining_elective.intersection(self.pass_courses)) > 0:

                self.remaining_elective = {None}

    def enroll_major(self, major):

        self.remaining_required = major.required_courses
        self.remaining_elective = major.elective_courses

    def pretty_table(self):

        return [self.cwid, self.name, self.major, sorted(self.pass_courses), self.remaining_required, self.remaining_elective]


class Instructor:

    def __init__(self, cwid, name, department):

        self.cwid = cwid
        self.name = name
        self.department = department
        self.courses = defaultdict(int)    # the key is course name,the value is number of students

    def add_students(self, course):

        self.courses[course] += 1

    def pretty_table(self):

        for course, num_stud in self.courses.items():
            yield [self.cwid, self.name, self.department, course, num_stud]


class Major:

    def __init__(self, department):

        self.department = department
        self.required_courses = set()  # set of major required courses
        self.elective_courses = set()  # set of major elective courses

    def add_course(self, course_code, flag):

        if flag.upper() == 'R':
            self.required_courses.add(course_code)

        elif flag.upper() == 'E':
            self.elective_courses.add(course_code)

        else:
            raise ValueError("The course {} is neither an elective or required course !".format(course_code))

    def pretty_table(self):

        return [self.department, sorted(self.required_courses), sorted(self.elective_courses)]


class Repository:

    def __init__(self, path):

        self.students = dict()
        self.instructors = dict()
        self.majors = dict()

        try:
            os.chdir(path)
        except FileNotFoundError:
            raise FileNotFoundError("the path isn't exist !")
        else:

            # set the path
            student_path = os.path.join(path, "students.txt")
            instructor_path = os.path.join(path, "instructors.txt")
            grades_path = os.path.join(path, "grades.txt")
            majors_path = os.path.join(path, "majors.txt")

            # open the file
            self.open_major_file(majors_path, '\t')
            self.open_stud_file(student_path, '\t')
            self.open_inst_file(instructor_path, '\t')
            self.open_grade_file(grades_path, '\t')

            # print the pretty table
            print('Majors Summary')
            self.print_pretty_table_major()
            print('\nStudents Summary')
            self.print_pretty_table_stud()
            print('\nInstructors Summary')
            self.print_pretty_table_inst()

    def open_major_file(self, file, split_type):

        expected_tokens = 3
        for major, flag, course_code in open_file(file, expected_tokens, '\t'):

            if major not in self.majors:
                self.majors[major] = Major(major)
            self.majors[major].add_course(course_code, flag)

    def open_stud_file(self, file, split_type):

        expected_tokens = 3
        for cwid, name, department in open_file(file, expected_tokens, '\t'):

            if department in self.majors:
                self.students[cwid] = Student(cwid, name, department)
                self.students[cwid].enroll_major(self.majors[department])

            else:
                raise ValueError("The major {} is not offered at the university.".format(department))

    def open_inst_file(self, file, split_type):

        expected_tokens = 3
        for cwid, name, department in open_file(file, expected_tokens, '\t'):
            self.instructors[cwid] = Instructor(cwid, name, department)

    def open_grade_file(self, file, split_type):

        expected_tokens = 4
        for cwid, course, grade, teacher in open_file(file, expected_tokens, '\t'):

            if cwid in self.students:
                self.students[cwid].add_course(course, grade)
            else:
                raise ValueError("Student with CWID: {} was never entered as a student".format(cwid))
            if teacher in self.instructors:
                self.instructors[teacher].add_students(course)
            else:
                raise ValueError("Instructor with CWID: {} was never entered as an instructor".format(teacher))

    def print_pretty_table_stud(self):

        pt = PrettyTable(field_names=['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives'])
        for cwid in self.students:
            pt.add_row(self.students[cwid].pretty_table())
        print(pt)

    def print_pretty_table_inst(self):

        pt = PrettyTable(field_names=['CWID', 'Name', 'Department', 'Course', 'Number of Students'])
        DB_File = 'C:\\Users\\54783\\Desktop\\810\\HW P11'
        db = sqlite3.connect(DB_File)
        for row in db.execute("""select cwid, name, dept, course, count(Student_CWID) as student_num from HW11_instructors join
                                 HW11_grades on HW11_instructors.cwid = hw11_grades.Instructor_CWID group by course"""):
            
            pt.add_row(row)

        print(pt)

    def print_pretty_table_major(self):

        pt = PrettyTable(field_names=['Dept.', 'Required', 'Electives'])
        for department in self.majors:
            pt.add_row(self.majors[department].pretty_table())
        print(pt)


def open_file(file, expected_tokens, split_type='\t'):
    try:
        fp = open(file, 'r')
    except FileNotFoundError:
        raise FileNotFoundError("Invalid File ({}). Please try again.".format(file))
    else:
        with fp:
            for line_number, line in enumerate(fp):
                line = line.strip().split(split_type)
                if len(line) == expected_tokens:
                    yield line
                else:
                    raise ValueError("There is an error in the format of line {}. Please refer to the proper formatting of the respective text file.".format(line_number))


def main():
    path = r'C:\Users\54783\Desktop\810\UniversityInfoDatabase-HW10\HW09data'
    stevens_information = Repository(path)


if __name__ == '__main__':
    main()