from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/instructor')
def instructor():

    sqlite_file = 'C:\\Users\\54783\\Desktop\\810\\HW P11'
    query = """select cwid, name, dept, course, count(Student_CWID) as student_num from HW11_instructors join
                                 HW11_grades on HW11_instructors.cwid = hw11_grades.Instructor_CWID group by course"""

    db = sqlite3.connect(sqlite_file)
    rows = db.execute(query)

    data = [{'cwid': cwid, 'name': name, 'dept': dept, 'course': course, 'student': student_num} for cwid, name, dept, course, student_num in rows]

    db.close()  

    return render_template(
        'instructor.html',
        title='Stevens Repository',
        table_title="Instructors information",
        instructors=data)


app.run(debug=True)