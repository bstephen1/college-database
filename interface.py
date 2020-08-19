#interface for jupiter college database

import MySQLdb
import argparse


parser = argparse.ArgumentParser(description = "Jupiter College database interface tool")
parser.add_argument("-q","--query", nargs = 1, type = int, help = "select one of the 10 queries to perform")
interaction = parser.add_mutually_exclusive_group()
interaction.add_argument("-a","--add", action = 'store_true', help = "add a row to a table")
interaction.add_argument("-e","--edit", action = 'store_true', help = "edit a row in a table")
interaction.add_argument("-d","--delete", action = 'store_true', help = "delete a row from a table")
args = parser.parse_args()

#set username and password
user = "root"
password = "root"
#open database connection
college = MySQLdb.connect("localhost", user, password, "jc")
cursor = college.cursor()


#add a new row to the database
if args.add :
	cursor.execute('show tables;')
	tables = cursor.fetchall()
	print "Select a table: "
	#prints names of all tables
	for x in range(len(tables)) :
		#2D array because fetchall() retuns each table as a list with one element
		print "%d -- %s" % (x, tables[x][0])
	x = int(raw_input())
	table = tables[x][0]
	
	cursor.execute('describe %s;' % (table))
	results = cursor.fetchall()
	values = []
	#if there is a connecting table
	values2 = []
	table2 = ""
	print "Enter %s fields: " % (table)
	#get input for each field 
	for x in range(len(results)) :
		if table == 'enrolled_courses' and results[x][0] == 'grade_received' : continue
		t = raw_input("%s [%s]: " % (results[x][0], results[x][1]))
		values.append(t)
	
	#constraints below
	
	#degree_programs -- director must be full-time
	if table == 'degree_programs' :
		dir_check = False
		while not dir_check :
			cursor.execute("select status from faculty where ID=%s;" % (values[2]))
			status = cursor.fetchone()
			if status[0] == 'full-time' :
				dir_check = True
			else :
				print "Director must be a full-time faculty member"
				dir = raw_input("Enter a valid director: ")
				values[2] = dir
				
	#departments -- chair must be full-time tenure-track, each department offers 1+ degree_programs, (implicit -- director must be full-time)
	if table == 'departments' :
		chair_check = False
		#chair must be full-time tenure-track
		while not chair_check :
			cursor.execute("select status, title_type from faculty where ID=%s;" % (values[1]))
			title_status = cursor.fetchone()
			if title_status[0] == 'full-time' and title_status[1] == 'tenure-track' :
				chair_check = True
			else :
				print "Department chair must be a full-time, tenure-track faculty member"
				chair = raw_input("Enter a valid chair: ")
				values[1] = chair
		#each department offers 1+ degree_programs (links to degree_program table)
		print "\nEnter degree_program fields: "
		table2 = "degree_program"
		cursor.execute('describe degree_programs;')
		results = cursor.fetchall()
		for x in range(len(results)) :
			if x == 3 :
				values2.append(values[0])
			else :
				t = raw_input("%s [%s]: " % (results[x][0], results[x][1]))
				values2.append(t)
		#director must be full-time
		dir_check = False
		while not dir_check :
			cursor.execute("select status from faculty where ID=%s;" % (values2[2]))
			status = cursor.fetchone()
			if status[0] == 'full-time' :
				dir_check = True
			else :
				print "Director must be a full-time faculty member"
				dir = raw_input("Enter a valid director: ")
				values2[2] = dir	
				
	if table == 'faculty' :
		cursor.execute('describe faculty_departments;')
		table2 = "faculty_departments"
		results = cursor.fetchall()
		values2.append(values[0])
		t = raw_input("%s [%s]: " % (results[1][0], results[1][1]))
		values2.append(t)
		
	#faculty_departments -- each full-time belongs to one department, part-time may belong to multiple
	if table == 'faculty_departments' :
		cursor.execute('select status from faculty where ID=%s;' % (values[0]))
		results = cursor.fetchone()
		if results[0] == 'full-time' :
			print 'Faculty must be part-time to belong to multiple departments. No changes saved.'
			exit()
		
	#course_offerings -- must have 1+ meeting periods
	if table == 'course_offerings' :
		table2 = "meeting_periods"
		cursor.execute('describe meeting_periods;')
		results = cursor.fetchall()
		print "\nEnter Meeting_periods fields: "
		for x in range(len(results)) :
			if x < 5 :
				values2.append(values[x])
			else :
				t = raw_input("%s [%s]: " % (results[x][0], results[x][1]))
				values2.append(t)
	
	#enrolled_courses -- students must satisfy 1+ prereqs before enrolling, may repeat at most 3 times
	if table == 'enrolled_courses' :
		student = values[0]
		ac = values[1]
		num = values[2]
		#satisfy prereqs
		cursor.execute("select * from enrolled_courses where student_id = \'%s\'" % (student))
		enrolled = cursor.fetchall()
		cursor.execute("select * from prerequisites where course_acronym = \'%s\' and course_num = \'%s\';" % (ac, num))
		prereqs = cursor.fetchall()
		check = True
		for x in range(len(prereqs)) :
			check = False
			for y in range(len(enrolled)) :
				#check course acronym, num -- if grade meets minimum, break
				if enrolled[y][1] == prereqs[x][0] and enrolled[y][2] == prereqs[x][1] and enrolled[y][6] and enrolled[y][6] != 'AU' and enrolled[y][6] != 'NG' and ord(enrolled[y][6]) <= ord(prereqs[x][4]) :
					check = True
					break
		if not check :
			print "Cannot enroll: prerequisite not met. No changes saved."
			exit()
		#repeat at most 3 times (4 total attempts)
		results = cursor.execute("select * from enrolled_courses where student_id=\'%s\' and course_num=\'%s\' and course_acronym='%s';" % (student, num, ac))
		if results > 4 :
			print "You may only repeat a course 3 times (4 total attempts). No changes saved."
			exit()
		
	#student_degrees -- must meet requirements to obtain degree, highest grade used for consideration
	if table == "student_degrees" :
		student = values[0]
		degree = values[1]
		#check if student meets minimum credits, courses (all courses assumed to be 3 credits)
		enrolled_courses = cursor.execute("select distinct course_acronym, course_num from enrolled_courses where student_ID = \'%s\' and not grade_received = 'W' and not grade_received = 'AU' and not grade_received = 'NG' and not grade_received = 'I';" % (student))
		cursor.execute("select required_credits, required_courses from degree_programs where name = \'%s\';" % (degree))
		required = cursor.fetchone()
		credits = required[0]
		courses = required[1]
		if not (enrolled_courses >= courses and enrolled_courses * 3 >= credits) :
			print "Student does not meet the minimum credit/course requirement. No changes saved."
			exit()
		#check if student meets coursework requirements (specific classes)
		cursor.execute("select course_acronym, course_num, min_grade from degree_programs join coursework_requirements on name = program_name where name = \'%s\';" % (degree))
		req_courses = cursor.fetchall()
		cursor.execute("select * from enrolled_courses where student_id = \'%s\'" % (student))
		enrolled = cursor.fetchall()
		check = False
		for x in range(len(req_courses)) :
			for y in range(len(enrolled)) :
				#check course acronym, num -- if grade meets minimum, break
				if enrolled[y][1] == req_courses[x][0] and enrolled[y][2] == req_courses[x][1] and enrolled[y][6] and enrolled[y][6] != 'AU' and enrolled[y][6] != 'NG' and ord(enrolled[y][6]) <= ord(req_courses[x][2]) :
					check = True
					break
		if not check :
			print "Cannot award degree: required classes not taken. No changes saved."
			exit()
		
	#students have 1+ programs_pursing
	if table == 'students' :
		print "\nEnter programs_pursuing fields: "
		table2 = "programs_pursuing"
		cursor.execute('describe programs_pursuing;')
		results = cursor.fetchall()
		for x in range(len(results)) :
			if x == 0 :
				values2.append(values[0])
			elif x == 2 :
				values2.append('no')
			else :
				t = raw_input("%s [%s]: " % (results[x][0], results[x][1]))
				values2.append(t)
	
	#commit changes to database if possible
	try :
		if table == 'enrolled_courses' : 
			cursor.execute("insert into %s values(\'%s\', null);" % (table, '\',\''.join(values)))
		else : 
			cursor.execute("insert into %s values(\'%s\');" % (table, '\',\''.join(values)))
		if values2 : cursor.execute("insert into %s values(\'%s\');" % (table2, '\',\''.join(values2)))
		college.commit()
		print "Changes saved."
	except :
		college.rollback()
		print "Error: could not commit changes. Check input fields. No changes saved."
		
	
#edit an existing row in the database. Cannot edit primary key fields
elif args.edit :
	cursor.execute('show tables;')
	tables = cursor.fetchall()
	print "Select a table: "
	#prints names of all tables
	for x in range(len(tables)) :
		#2D array because fetchall() retuns each table as a list with one element
		print "%d -- %s" % (x, tables[x][0])
	x = int(raw_input())
	table = tables[x][0]

	#get the field to update
	cursor.execute('describe %s;' % (table))
	fields = cursor.fetchall()
	print "Select a field: "
	for x in range(len(fields)) :
		if fields[x][3] != "PRI" :
			#2D array because fetchall() retuns each field as a list with one element
			print "%d -- %s" % (x, fields[x][0])
	y = int(raw_input())
	field = fields[y][0]
	
	#get row to update
	print "Enter primary key of row to update: "
	pkey = []
	for x in range(len(fields)) :
		if fields[x][3] == "PRI" :
			#2D array because fetchall() retuns each field as a list with one element
			pkey.append(fields[x][0] + " = \'" + raw_input("%s [%s]: " % (fields[x][0], fields[x][1])))
			
	#updated value
	new_value = raw_input("New value for %s [%s]: " % (field, fields[y][1]))

	#commit changes to database if possible
	try :
		cursor.execute("update %s set %s = \'%s\' where %s\';" % (table, field, new_value, "\' and ".join(pkey)))
		college.commit()
		print "Changes saved."
	except :
		college.rollback()
		print "Error: could not commit changes. Check input fields. No changes saved."

		
#delete a row from the database
elif args.delete :
	cursor.execute('show tables;')
	tables = cursor.fetchall()
	print "Select a table: "
	#prints names of all tables
	for x in range(len(tables)) :
		#2D array because fetchall() retuns each table as a list with one element
		print "%d -- %s" % (x, tables[x][0])
	x = int(raw_input())
	table = tables[x][0]
	
	#row to delete
	print "Enter primary key of row to delete: "
	pkey = []
	cursor.execute('describe %s;' % (table))
	fields = cursor.fetchall()
	for x in range(len(fields)) :
		if fields[x][3] == "PRI" :
			#2D array because fetchall() retuns each field as a list with one element
			pkey.append(fields[x][0] + " = \'" + raw_input("%s [%s]: " % (fields[x][0], fields[x][1])))

	#commit changes to database if possible
	try :
		cursor.execute("delete from %s where %s\';" % (table, "\' and ".join(pkey)))
		college.commit()
		print "Changes saved."
	except :
		college.rollback()
		print "Error: could not commit changes. Check foreign key constraints. No changes saved."
		

#queries
elif args.query :
	
	q = args.query[0]
	#the 10 queries, as numbered in the requirements sheet
	if q == 1 :
		#list all faculy, by department
		cursor.execute("select * from faculty join faculty_departments on id=faculty_id order by department_name;")
		results = cursor.fetchall()
		print "\nFaculty: "
		for row in results :
			print row
		
	elif q == 2 :
		#number of faculty and courses for a department
		dep = raw_input("Enter a department: ")
		faculty = cursor.execute("select * from faculty_departments where department_name = \'%s\';" % dep)
		courses = cursor.execute("select * from degree_programs join courses on degree_programs.acronym = courses.acronym where department = \'%s\';" % dep)
		print "Faculty in %s: %s\nCourses in %s: %s" % (dep, faculty, dep, courses)
	
	elif q == 3 :
		#number of course offerings for a department and date
		dep = raw_input("Enter a department: ")
		sem = raw_input("Enter a semester: ")
		year = raw_input("Enter a year: ")
		courses = cursor.execute("select * from degree_programs join course_offerings on acronym = course_acronym where department = \'%s\' and semester_offered = '\%s\' and year_offered = \'%s\';" % (dep, sem, year))
		print "Number of courses in %s during %s %s: %s" % (dep, sem, year, courses)
		
	elif q == 4 :
		ac = raw_input("Enter the course acronym: ")
		num = raw_input("Enter the course num: ")
		sec = raw_input("Enter the section num: ")
		sem = raw_input("Enter a semester: ")
		year = raw_input("Enter a year: ")
		#names of students enrolled in this course
		cursor.execute("select first_name, last_name from students join enrolled_courses on id=student_id where course_acronym = \'%s\' and course_num = \'%s\' and section_num = \'%s\' and semester_offered = \'%s\' and year_offered = \'%s\';" % (ac, num, sec, sem, year))
		results = cursor.fetchall()
		print "\nStudents enrolled: "
		for row in results :
			print row
		
	elif q == 5 :
		sem = raw_input("Enter a semester: ")
		year = raw_input("Enter a year: ")
		
		#get all majors
		cursor.execute("select name from degree_programs;")
		majors = cursor.fetchall()
		
		print "\nStudents X Credits for each major: "
		#gets the amount of credits all students with the given major are taking in the given semester
		for row in majors :
			sum = 3 * cursor.execute("select * from enrolled_courses join programs_pursuing on enrolled_courses.student_id = programs_pursuing.student_id where program_name = \'%s\' and program_dropped = \'no\' and semester_offered = \'%s\' and year_offered = \'%s\';" % (row[0], sem, year))
			print "%s: %s" % (row[0], sum)
			
	
	elif q == 6 :
		sem = raw_input("Enter a semester: ")
		year = raw_input("Enter a year: ")
		
		#get all departments
		cursor.execute("select distinct department from degree_programs;")
		deps = cursor.fetchall()
		
	
		print "\nStudents X Credits for each department: "
		#gets the amount of credits all students with the given department are taking in the given semester
		for row in deps :	
			print "%s:" % row[0]
			#get all majors in the department
			cursor.execute("select name from degree_programs where department = \'%s\';" % row[0])
			majors = cursor.fetchall()
			for row in majors :
				sum = 3 * cursor.execute("select * from enrolled_courses join programs_pursuing on enrolled_courses.student_id = programs_pursuing.student_id where program_name = \'%s\' and program_dropped = \'no\' and semester_offered = \'%s\' and year_offered = \'%s\';" % (row[0], sem, year))
				print "\t%s: %s" % (row[0], sum)
			print
	
	elif q == 7 :
		prog = raw_input("Enter a degree program: ")
		sem = raw_input("Enter a semester: ")
		year = raw_input("Enter a year: ")
		#gpa of each student during given semester for courses from the given program
		cursor.execute("select student_ID, grade_received from enrolled_courses join degree_programs on acronym=course_acronym where name=\'%s\' and year_offered = \'%s\' and semester_offered=\'%s\';" % (prog, year, sem))
		
		results = cursor.fetchall()
		students = {}
		#get a dictionary of all student grades
		for x in range(len(results)) :
			if results[x][0] in students :
				students[results[x][0]].append(results[x][1])
			else :
				students[results[x][0]] = [results[x][1]]
		#compute the gpa
		print "Student   GPA"
		for x in students :
			gpa = 0
			for y in students[x] :
				if y == 'A' : gpa += 4
				elif y == 'B' : gpa += 3
				elif y == 'C' : gpa += 2
				elif y == 'D' : gpa += 1
			gpa /= len(students[x]) * 1.
			print "%s   %s" % (x, gpa)
	
	elif q == 8 :
		ac = raw_input("Enter the course acronym: ")
		num = raw_input("Enter the course num: ")
		sec = raw_input("Enter the section num: ")
		sem = raw_input("Enter a semester: ")
		year = raw_input("Enter a year: ")
		#all students enrolled in the class
		cursor.execute("select student_id from enrolled_courses where course_acronym= \'%s\' and course_num= \'%s\' and section_num = \'%s\' and semester_offered = \'%s\' and year_offered = \'%s\';" % (ac, num, sec, sem, year))
		students = cursor.fetchall()
		
		#all prereqs for the class
		cursor.execute("select prereq_acronym, prereq_num, min_grade from prerequisites where course_acronym = \'%s\' and course_num = \'%s\';" % (ac, num))
		prereqs = cursor.fetchall()
		
		#prereqs that the student has enrolled in
		print "Students who have met all prereqs: "
		for s in students :
			check = True
			for p in prereqs :
				cursor.execute("select grade_received from enrolled_courses where student_id = \'%s\' and course_acronym = \'%s\' and course_num = \'%s\';" % (s[0], p[0], p[1]))
				grades = cursor.fetchall()
				min_grade = p[2]
				for grade in grades :
					#check for a course that meets the min grade
					g = grade[0]
					if (g == 'A' or g == 'B' or g == 'C' or g == 'D' or g == 'F') and ord(g) <= ord(min_grade) :
						break
					check = False
			if check : print s[0]
			
	elif q == 9 :
		
		#get all the programs
		cursor.execute("select name from degree_programs;")
		programs = cursor.fetchall()
		
		#get number of students per program
		print "Number of students pursuing each degree program: "
		for x in programs :
			program = x[0]
			num = cursor.execute("select * from programs_pursuing where program_dropped = \'no\' and program_name = \'%s\';" % program)
			print "%s: %d" % (program, num)
	
	elif q == 10 :
		
		#get the courses
		dp = raw_input("Enter the name of a degree program: ")
		cursor.execute("select acronym, num from courses where program_name = \'%s\';" % dp)
		courses = cursor.fetchall()
		
		#get years
		start = raw_input("Enter the starting year: ")
		end = raw_input("Enter the ending year: ")
		
		for row in courses :
			#get grades for a course in the list
			cursor.execute("select grade_received from enrolled_courses where course_acronym = \'%s\' and course_num = \'%s\' and grade_received and year_offered between \'%s\' and \'%s\';" % (row[0], row[1], start, end))
			results = cursor.fetchall()
			grades = []
			for g in range(len(results)) :
				x = results[g][0]
				if x == 'A' or x == 'B' or x == 'C' or x == 'D' or x == 'F' :
					#turn them into a number
					x = (ord(x) - ord('A')) * -1 + 4 
				else :
					x = 0
				grades.append(x)
			if grades :
				mean = float(sum(grades)) / len(grades)
				#std dev
				sigma = 0
				for x in grades :
					sigma += pow(x - mean, 2)
				dev = pow(sigma / float(len(grades)), .5)
				print "%s %s:\n\tmin: %s\n\tmax: %s\n\tavg: %s\n\tdev: %s" % (row[0], row[1], min(grades), max(grades), mean, dev)
			else : 
				print "%s %s:\n\tmin: %s\n\tmax: %s\n\tavg: %s\n\tdev: %s" % (row[0], row[1], 0, 0, 0, 0)
			
		
