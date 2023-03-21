from flask import Flask, request, redirect
from flask.templating import render_template
#from flask_migrate import Migrate, migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True

# configuration for sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
#migrate = Migrate(app, db)

class Gradebook(db.Model):
    # student_id: id of student who is taking course
    # course_id: id of course being taken by student
    # grade: integer score for student (with student_id) in course (with course_id)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False, primary_key=True)
    grade = db.Column(db.Integer, unique=False, nullable=False)

    # like toString
    #def __repr__(self):
    #    return f"Student Id: {self.student_id}, Course Id: {self.course_id}, Student Grade: {self.grade}"

class Student(db.Model):
    # Id: unique id for each student
    # name: first and last name of student
    # credits: # of credits earned by student
    # courses_details: points to Gradebook model keeping track of student's courses and corresponding grades
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    courses_details = db.relationship('Gradebook')

    # like toString
    #def __repr__(self):
    #    return f"Id: {self.id}, Name: {self.name}, Credits: {self.credits}"

class Instructor(db.Model):
    # Id: unique id for each instructor
    # name: first and last name of instructor
    # department: name of department instructor is in
    # courses: points to Course model for each course instructor is teaching
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    department = db.Column(db.String(20), unique=False, nullable=False)
    courses = db.relationship('Course', backref='instructor')

    # like toString
    #def __repr__(self):
    #    return f"Id: {self.id}, Name: {self.name}, Department: {self.department}"

class Course(db.Model):
    # Id: unique class id for each course
    # title: course title
    # instructor_id: unique id for instructor teaching course
    # enrollment_details: points to Gradebook model keeping track of student's courses and corresponding grades
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=False, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'), nullable=True)
    enrollment_details = db.relationship('Gradebook')

    # like toString
    #def __repr__(self):
    #    return f"Id: {self.id}, Title: {self.title}, Instructor Id: {self.instructor_id}"

# home
@app.route('/')
def index():
    # load all current data
    students = Student.query.all()
    instructors = Instructor.query.all()
    courses = Course.query.all()
    # reference index.html for page format
    return render_template('index.html', students=students, instructors=instructors, courses=courses)

@app.route('/create', methods=["POST"])
def create():
    # data from the form to be stored in database
    input1 = request.form.get("input1")
    input2 = request.form.get("input2")
    input3 = request.form.get("input3")
    info_type = request.form.get("type")

    # check that they are not null, then add according to type
    if input1 and input2 and input3:
        if info_type == 'student':
            student = Student(id=input1, name=input2, credits=input3)
            db.session.add(student)
        elif info_type == 'instructor':
            instructor = Instructor(id=input1, name=input2, department=input3)
            db.session.add(instructor)
        elif info_type == 'course':
            # make sure instructor exists
            instructor = Instructor.query.get(input3)
            if instructor:
                course = Course(id=input1, title=input2, instructor_id=input3)
                db.session.add(course)
        db.session.commit()
    return redirect('/')

@app.route('/delete/<string:type>/<int:id>')
def delete(type, id):
    # check type, then delete if id is valid
    if type == 'student':
        student = Student.query.get(id)
        if student:
            for course in student.courses_details:
                db.session.delete(course)
            db.session.delete(student)
    elif type == 'instructor':
        instructor = Instructor.query.get(id)
        if instructor:
            db.session.delete(instructor)
    elif type == 'course':
        course = Course.query.get(id)
        if course:
            for student in course.enrollment_details:
                db.session.delete(student)
            db.session.delete(course)

    db.session.commit()
    return redirect('/')

@app.route('/modify', methods=["GET", "POST"])
def modify():
    # check type, then, if info is valid, delete old version of model and create new version 
    type = request.form.get('mod-type')
    if type == 'student':
        id = request.form.get('mod-student-1-hidden')
        student = Student.query.get(id)

        # check validity of request and student
        if request.method == 'POST' and student:
            # course_info saves course id and grade for new student instance
            course_info = []
            for course in student.courses_details:
                course_info.append((course.course_id, course.grade))
                # remove dependence
                db.session.delete(course)

            # delete old student instance
            db.session.delete(student)
            db.session.commit()

            # get updated information to create new student instance
            name = request.form.get('mod-student-2')
            credits = request.form.get('mod-student-3')
            student = Student(id=id, name=name, credits=credits)
            db.session.add(student)

            # add old course info to new student instance
            for x in range(len(course_info)):
                gradebook = Gradebook(student_id=id, course_id=course_info[x][0], grade=course_info[x][1])
                student.courses_details.append(gradebook)
                course = Course.query.get(course_info[x][0])
                course.enrollment_details.append(gradebook)
            db.session.commit()
    elif type == 'instructor':
        id = request.form.get('mod-instructor-1-hidden')
        instructor = Instructor.query.get(id)

        # check validity of request and instructor
        if request.method == 'POST' and instructor:
            # courses saves course id for new instructor instance
            courses = []
            for course in instructor.courses:
                courses.append(course)

            # delete old instructor instance
            db.session.delete(instructor)
            db.session.commit()

            # get updated information to create new instructor instance
            name = request.form.get('mod-instructor-2')
            department = request.form.get('mod-instructor-3')
            instructor = Instructor(id=id, name=name, department=department)
            db.session.add(instructor)

            # add old course info to new instructor instance
            for course in courses:
                instructor.courses.append(course)
            db.session.commit()
    elif type == 'course':
        id = request.form.get('mod-course-1-hidden')
        course = Course.query.get(id)

        # check validity of request and course
        if request.method == 'POST' and course:
            # student_info saves course id and grade for new course instance
            student_info = []
            for student in course.enrollment_details:
                student_info.append((student.student_id, student.grade))
                # remove dependence
                db.session.delete(student)

            # delete old course instance
            db.session.delete(course)
            db.session.commit()

            # get updated information to create new course instance
            title = request.form.get('mod-course-2')
            instructor_id = request.form.get('mod-course-3')
            course = Course(id=id, title=title, instructor_id=instructor_id)
            db.session.add(course)

            # add old student info to new course instance
            for x in range(len(student_info)):
                gradebook = Gradebook(student_id=student_info[x][0], course_id=id, grade=student_info[x][1])
                course.enrollment_details.append(gradebook)
                student = Student.query.get(student_info[x][0])
                student.courses_details.append(gradebook)
            db.session.commit()
    return redirect('/')

@app.route('/modify_grade', methods=["GET", "POST"])
def modify_grade():
    # delete previous gradebook instance
    info = request.form.get('student-id').split(',')
    student_id = info[0]
    course_id = info[1]
    student = Student.query.get(student_id)
    this_course = student.courses_details[0]

    # iterate through students courses to find course with course_id
    for course in student.courses_details:
        if int(course.course_id) == int(course_id):
            this_course = course
    db.session.delete(this_course)
    db.session.commit()
    
    # create new gradebook instance with new grade
    new_grade = request.form.get('mod-grade')
    gradebook = Gradebook(student_id=student_id, course_id=course_id, grade=new_grade)
    db.session.add(gradebook)

    # configure gradebook instance to reference correct student and course
    student.courses_details.append(gradebook)
    course = Course.query.get(course_id)
    course.enrollment_details.append(gradebook)
    db.session.commit()
    return redirect('/')

@app.route('/student_add_remove_course', methods=["GET", "POST"])
def student_add_remove_course():
    # if course id is valid, add or remove course for student
    student_id = request.form.get("add-remove-sid")
    course_id = request.form.get("add-remove-cid")
    this_student = Student.query.get(student_id)
    this_course = Course.query.get(course_id)

    # check valid course
    if this_course:
        enrolled = False
        # if student is already enrolled in course, remove student from course
        if this_student.courses_details:
            gradebook_to_delete = this_student.courses_details[0]
            for course in this_student.courses_details:
                if int(course.course_id) == int(course_id):
                    enrolled = True
                    gradebook_to_delete = course
                    break
            if enrolled:
                db.session.delete(gradebook_to_delete)

        # if student is not already enrolled in the course, add student to course
        if not enrolled:
            new_gradebook = Gradebook(student_id=student_id, course_id=course_id, grade=100)
            this_student.courses_details.append(new_gradebook)
            this_course.enrollment_details.append(new_gradebook)
        db.session.commit()
    return redirect('/')

@app.route('/instructor_add_remove_course', methods=["GET", "POST"])
def instructor_add_remove_course():
    instructor_id = request.form.get("add-remove-iid")
    course_id = request.form.get("add-remove-cid")
    this_instructor = Instructor.query.get(instructor_id)
    this_course = Course.query.get(course_id)
    
    # check course validity
    if this_course:
        teaching = False
        # search for course to see if instructor is already teaching it
        for course in this_instructor.courses:
            if int(course.id) == int(course_id):
                teaching = True
        # if teaching, remove
        if teaching:
            this_instructor.courses.remove(this_course)
        # if not teaching, add
        else:
            this_instructor.courses.append(this_course)
        db.session.commit()
    return redirect('/')


if __name__ == '__main__':    
    app.run()