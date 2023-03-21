from app import app, db, Student, Course, Instructor, Gradebook

app.app_context().push()
db.drop_all()
db.create_all()

# Instructors
instructor1 = Instructor(id=456 , name="Jim George" , department="Statistics")
db.session.add(instructor1)
instructor2 = Instructor(id=589 , name="Kevin Matthews" , department="Information Systems")
db.session.add(instructor2)
instructor3 = Instructor(id=821 , name="John Sullins" , department="Health Sciences")
db.session.add(instructor3)
instructor4 = Instructor(id=954 , name="William Robertson" , department="Physics")
db.session.add(instructor4)
instructor5 = Instructor(id=673 , name="Sandra Wilson" , department="Biology")
db.session.add(instructor5)
instructor6 = Instructor(id=535 , name="Donna Joseph" , department="Computer Science")
db.session.add(instructor6)
instructor7 = Instructor(id=990 , name="Natalia Smith" , department="Chemistry")
db.session.add(instructor7)

# Courses
course1 = Course(id=9076, title="Software Engineering", instructor_id=535)
db.session.add(course1)
course2 = Course(id=1028, title="Organic Chemistry I", instructor_id=990)
db.session.add(course2)
course3 = Course(id=7654, title="Health Informatics", instructor_id=821)
db.session.add(course3)
course4 = Course(id=8721, title="Database Systems", instructor_id=589)
db.session.add(course4)

# assigning courses to instructors
instructor6.courses.append(course1)
instructor7.courses.append(course2)
instructor3.courses.append(course3)
instructor2.courses.append(course4)

# Students
student1 = Student(id=387 , name="John Walker", credits=93)
db.session.add(student1)
student2 = Student(id=209 , name="David Jameson", credits=87)
db.session.add(student2)
student3 = Student(id=101 , name="Emma Wells", credits=57)
db.session.add(student3)
student4 = Student(id=190 , name="Nisha Singh", credits=92)
db.session.add(student4)
student5 = Student(id=978 , name="Jack Thompson", credits=100)
db.session.add(student5)
student6 = Student(id=350 , name="Ben Joseph", credits=79)
db.session.add(student6)
student7 = Student(id=270 , name="Kate Jimpson", credits=68)
db.session.add(student7)

# Gradebook pages
gradebook_s1_c1 = Gradebook(student_id=student1.id, course_id=course1.id, grade=100)
db.session.add(gradebook_s1_c1)
gradebook_s1_c4 = Gradebook(student_id=student1.id, course_id=course4.id, grade=100)
db.session.add(gradebook_s1_c4)
gradebook_s2_c1 = Gradebook(student_id=student2.id, course_id=course1.id, grade=100)
db.session.add(gradebook_s2_c1)
gradebook_s2_c4 = Gradebook(student_id=student2.id, course_id=course4.id, grade=100)
db.session.add(gradebook_s2_c4)
gradebook_s2_c3 = Gradebook(student_id=student2.id, course_id=course3.id, grade=100)
db.session.add(gradebook_s2_c3)
gradebook_s3_c1 = Gradebook(student_id=student3.id, course_id=course1.id, grade=100)
db.session.add(gradebook_s3_c1)
gradebook_s3_c4 = Gradebook(student_id=student3.id, course_id=course4.id, grade=100)
db.session.add(gradebook_s3_c4)
gradebook_s4_c2 = Gradebook(student_id=student4.id, course_id=course2.id, grade=100)
db.session.add(gradebook_s4_c2)
gradebook_s4_c3 = Gradebook(student_id=student4.id, course_id=course3.id, grade=100)
db.session.add(gradebook_s4_c3)
gradebook_s5_c2 = Gradebook(student_id=student5.id, course_id=course2.id, grade=100)
db.session.add(gradebook_s5_c2)
gradebook_s6_c3 = Gradebook(student_id=student6.id, course_id=course3.id, grade=100)
db.session.add(gradebook_s6_c3)
gradebook_s7_c1 = Gradebook(student_id=student7.id, course_id=course1.id, grade=100)
db.session.add(gradebook_s7_c1)


# configuring gradebook pages
student1.courses_details.append(gradebook_s1_c1)
course1.enrollment_details.append(gradebook_s1_c1)

student1.courses_details.append(gradebook_s1_c4)
course4.enrollment_details.append(gradebook_s1_c4)

student2.courses_details.append(gradebook_s2_c1)
course1.enrollment_details.append(gradebook_s2_c1)

student2.courses_details.append(gradebook_s2_c4)
course4.enrollment_details.append(gradebook_s2_c4)

student2.courses_details.append(gradebook_s2_c3)
course3.enrollment_details.append(gradebook_s2_c3)

student3.courses_details.append(gradebook_s3_c1)
course1.enrollment_details.append(gradebook_s3_c1)

student3.courses_details.append(gradebook_s3_c4)
course4.enrollment_details.append(gradebook_s3_c4)

student4.courses_details.append(gradebook_s4_c2)
course2.enrollment_details.append(gradebook_s4_c2)

student4.courses_details.append(gradebook_s4_c3)
course3.enrollment_details.append(gradebook_s4_c3)

student5.courses_details.append(gradebook_s5_c2)
course2.enrollment_details.append(gradebook_s5_c2)

student6.courses_details.append(gradebook_s6_c3)
course3.enrollment_details.append(gradebook_s6_c3)

student7.courses_details.append(gradebook_s7_c1)
course1.enrollment_details.append(gradebook_s7_c1)

db.session.commit()