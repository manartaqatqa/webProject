
import datetime


db.define_table('courses',
	Field('code', 'string', required=True, notnull=True),
	Field('name', 'string'),
	Field('description', 'string'),
	Field('prerequisites', 'string', 'reference courses',requires=IS_IN_DB(db, 'courses.code', '%(name)s')),
	Field('instructor', 'string'),
	Field('capacity', 'integer'),
	Field('scheduled', 'integer','reference courseschedules',requires=IS_IN_DB(db, 'courseschedules.id', '%(days)s- %(startTime)s - %(endTime)s')),
	primarykey=['code'],
	migrate=False)


db.define_table('students',
	Field('id', 'string'),
	Field('fname', 'string'),
	Field('lname', 'string'),
	Field('email', 'string'),
	Field('password', 'string'),
	Field('registration_key','string'),
	Field('reset_password_key','string'),
	Field('registration_id','string'),
	migrate=False)

db.define_table('studentsreg',
	Field('id', 'integer', required=True, notnull=True),
	Field('studentId','integer'),
	Field('courseId','string'),
	primarykey=['id'],
	migrate=False)



db.define_table('rooms',
	Field('code', 'string', required=True, notnull=True),
	primarykey=['code'],
	migrate=True)


db.define_table('courseschedules',
	Field('id', 'integer',required=True, notnull=True),
	Field('days', 'string',requires=IS_IN_SET(['m,w', 's,tu,th'])),
	Field('startTime', 'time', default=datetime.time(0,0)),
	Field('endTime', 'time', default=datetime.time(0,0)),
	Field('RoomNo', 'string', 'reference rooms', requires=IS_IN_DB(db, 'rooms.code', '%(code)s')),
	primarykey=['id'],
	migrate=False
	) 