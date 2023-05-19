def student_completed_prerequisites(course, student_id):
    if not courses.prerequisites:
        return True

    completed_courses = db((db.registration.courses == db.courses.id) &
                            (db.registration.student == student_id) &
                            (db.registration.status == 'completed')).select(db.courses.ALL)
    completed_course_ids = [c.id for c in completed_courses]

    for prereq in course.prerequisites:
        if prereq not in completed_course_ids:
            return False

    return True

def course():
   
   
    fields = [
        db.courses.code,db.courses.name,db.courses.description,db.courses.prerequisites,db.courses.instructor,db.courses.capacity,db.courseschedules.days,db.courseschedules.startTime,db.courseschedules.endTime,db.courseschedules.RoomNo,
    ]

    def add_link(row):
        if row.courses.available == 0:
            return SPAN("  -")
        else:
            return A('Add', _href=URL('add_course', vars=dict(code=row.courses.code)))

    links = [add_link]

    grid = SQLFORM.grid(db.courses, fields=fields, links=links, create=False, editable=False, deletable=False, csv=False, details=False, searchable=fields)
    return dict(grid=grid)




def display_course_schedule():
    student_id = request.vars.studentid

    courses = db((db.courses.code == db.courses) &
                 (db.students.student_id == student_id)).select(db.courses.ALL)

    return dict(courses=courses)

def index():

    courses = db(db.courses).select()


    student_id = request.vars.studentid

    form = SQLFORM.factory(
        Field('courseid', 'integer', label='Course ID'),
        Field('studentid', 'integer', default=student_id, readable=False, writable=False),
        submit_button='Add Course',
    )

    if form.process().accepted:
        response.flash = add_course_to_schedule()
        course_schedule = display_course_schedule()

    return dict(form=form, course_schedule=course_schedule,courses=courses)


@auth.requires_login()
def add_course():
    if db.students(auth.user.id).typeu == 'student':
        course_id = request.vars.code
        student_id = auth.user.id
        
        course = db(db.courses.code == course_id).select().first()
        schedule = db(db.courseschedules.id == course.scheduled).select().first()

       
        conflicting_course = db(
            (db.studentsreg.studentID == student_id) & (db.studentsreg.status == "inProgress") & (db.studentsreg.courseID == db.courses.code) &
            (db.courses.scheduled == db.courseschedules.id) & (db.courseschedules.days == schedule.days) & 
            ((db.courseschedules.startTime <= schedule.startTime) & (schedule.startTime < db.courseschedules.endTime) |
             (db.courseschedules.startTime < schedule.endTime) & (schedule.endTime <= db.courseschedules.endTime))).select().first()
        
        if conflicting_course is not None:
            session.flash = 'Error: Course {} conflicts with course {} on {} from {} to {}'.format(
                course.name, 
                conflicting_course.courses.name, 
                schedule.days, 
                conflicting_course.courseschedules.startTime, 
                conflicting_course.courseschedules.endTime
            )
            redirect(URL('course', 'courses'))
        
        student_reg = db(db.studentsreg).select(orderby=~db.studentsreg.id).first()
        if student_reg is None:
            id = 1
        else:
            id = student_reg.id + 1 
        db.studentsreg.insert(id=id, studentID=student_id, courseID=course_id, status="inProgress")

        redirect(URL('coursereg', 'course'))

    else:
        redirect(URL('default', 'error'))