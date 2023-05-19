# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----

# default.py

def home():
    return locals()

def signuptest():
    form = SQLFORM(db.students)

    if form.process().accepted:
        # Student data is valid, insert it into the database
        response.flash = 'Registration successful!'
        redirect(URL('default', 'login'))

    return dict(form=form)


def display_form():
    form = FORM('Your name:', INPUT(_name='name'), INPUT(_type='submit'))
    return dict(form=form)


def index():
    
    courses = db.executesql("SELECT * FROM courses", as_dict=True)

    return dict(courses=courses)


def set_session():
    session.username="MANAR"
    return locals()

def get_session():
    username=session.username
    return locals();

def create_cookie():
    if db.students(auth.user.id).typeuser != 'instructor' and  db.students(auth.user.id).typeuser != 'student':
        response.cookies['webpro-cookie'] = response.session_id
        response.cookies['webpro-cookie']['expires'] = 1800
        return locals()
    else:
        redirect(URL('default', 'error'))



@auth.requires_login()
def get_cookie():
        username = str(auth.user.id)

        mycookie = request.cookies.get(username)
        name = mycookie
        return locals()

def list_students():

    students = db.executesql("SELECT * FROM students", as_dict=True)

    return dict(students=students)

def addStudentForm():

    form = SQLFORM(db.students)
    if form.process().accepted:
       response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'

    return dict(form=form)

def students():
    grid = SQLFORM.grid(db.students)

    return dict(grid=grid)


def add_user():

    name = request.vars['name']
    email = request.vars['email']

    return locals()
    

def addSchedule():

    form = SQLFORM(db.courseschedules)
    if form.process().accepted:
       response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'

    return dict(form=form)

def courses():
    if  db.students(auth.user.id).typeuser == 'student':
        query = (db.courses.scheduled == db.courseschedules.id)
        fields = [db.courses.code,db.courses.name,db.courses.capacity,db.courses.available,db.courses.instructor,db.courses.description,db.courseschedules.days,db.courseschedules.startTime,db.courseschedules.endTime,db.courseschedules.RoomNo,]
        grid = SQLFORM.grid(query,fields=fields,csv=False, create=False,searchable=fields)
        return dict(grid=grid)
    else:
        redirect(URL('default', 'error'))

def addCourse():


    form = SQLFORM(db.courses)
    if form.process().accepted:
       response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'

    return dict(form=form)

def addCourseForm():

    form = SQLFORM(db.courses)
    if form.process().accepted:
       response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'


def addStudent():

    if request.vars['fname']:
        first_name = request.vars['fname']
        last_name = request.vars['lname']
        email = request.vars['email']

        db.executesql("INSERT INTO students (first_name, last_name, email) VALUES (%s, %s, %s)", placeholders=(first_name,last_name, email))
    else:
        redirect(URL('addStudentForm'))

    return locals()

def details():

    if request.vars['id']:
        id = request.vars['id']
        students = db.executesql("SELECT * FROM students WHERE id=" + id, as_dict=True)

    return dict(student=students[0], students=students)


def delete():

    if request.vars['id']:
        id = request.vars['id']

        db.executesql("DELETE FROM students WHERE id=" + id)
    
    redirect(URL('list_students'))


def search():
    query = request.vars.query
    if not query:
        courses =[]
    else:
        courses = db(db.courses.name.contains(query) | db.courses.code.contains(query) | db.courses.instructor.contains(query)).select()
    return dict(courses=courses ,query=query)

def student():
    query=request.vars.query
    if not query:
        students=[]
    else:
        students=db(db.students.fname.contains(query) | db.students.id.contains(query))
    return dict(student=student,query=query)

def details():
    code=request.args(0)
    courses=(db.courses.ALL)
    return dict(courses=courses)





# def courseForm():
#     return locals()

# def addStudent():
#     if request.vars['name']:
#         name=request.vars['name']
#         year=request.vars['year']
#         db.executesql("db.executesql("INSERT INTO students (first_name, last_name, email) VALUES (%s, %s, %s)", placeholders=(first_name,last_name, email)) ")

# def search_courses():
#     form = SQLFORM.factory(Field("search_query", label="Search by course code, name, or instructor"))
#     courses = []
#     if form.process().accepted:
#         query = form.vars.search_query
#         courses = db((db.courses.course_code.contains(query)) | (db.courses.course_name.contains(query)) | (db.courses.instructor_name.contains(query))).select()
#     return dict(form=form, courses=courses)

# def addCourses():
#     form=SQLFORM(db.courses)
#     if form.process().accepted:
#         response.flash="the form is correct"
#     elif form>errors:
#     else:
#         response.flash=""

# def test():
#     cname="priciples of compilers"
#     query = f""" 
#     SELECT * FROM COURSES
#     WHERE NAME='{cname}'
#     """
#     print(query)
#     courses= db.executesql(query,as_dict=True)
# def addStudentForm():
#     return locals();
    
    


# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    auth.settings.login_next = URL('home')
    auth.settings.register_next = URL( 'home')
    """
    

    if auth().process().accepted:
        session.secure() 
        auth.settings.expiration = 1800
        response.cookies['username'] = auth.user.first_name
        response.cookies['username']['expires'] = 1800
        redirect(URL('default/dashboard'))

    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
