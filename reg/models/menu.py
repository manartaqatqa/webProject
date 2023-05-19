# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'home'), [])
]

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if not configuration.get('app.production'):
    _app = request.application
    response.menu += [
        (T('Schedules'), False, URL('regs','schedules')),
        (T('Add Schedule'), False, URL('/addSchedule')),
        (T('Courses'), False, URL('regs','courses')),
        (T('Add Course'), False, URL('regs','addCourse')),
        (T('add course to schedule'), False, URL('coursereg','course')),
        (T('list students'), False, URL('default','list_students')),


    ]

