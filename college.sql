
create database jc;
use jc;

create table students(
	ID char(7) not null unique,
	primary key (ID), 
	first_name varchar(30) not null,
	last_name varchar(30) not null,
	gender enum('m', 'f') not null,
	date_of_birth date not null, 
	matriculation_date date not null,
	hsgpa decimal(3, 2) not null,
	hsgraduation year not null,
	hsName varchar(50) not null,
	hsState varchar(15) not null, 
	hsZip int(5) not null 
);


create table faculty(
	ID char(5) not null unique,
	primary key (ID),
	first_name varchar(30),
	last_name varchar(30),
	email varchar(30), 
	telephone varchar(30) not null,
	title enum('instructor', 'lecturer', 'senior lecturer', 'assistant professor', 'associate professor', 'professor'),
	status enum('full-time', 'part-time'),
	title_type enum('tenure-track', 'non-tenure-track', 'visiting', 'adjunct'),
	highest_degree varchar(30),
	discipline_highest_degree varchar(30)
);


create table departments(
	name varchar(30) unique not null,
	primary key (name),
	chair char(5) not null,
	foreign key (chair) references faculty(ID) on delete cascade,
	room_number int(3) not null,
	building_code char(4) not null,
	telephone varchar(30) not null
);


create table faculty_departments(
	faculty_ID char(5) not null,
	foreign key (faculty_ID) references faculty(ID) on delete cascade,
	department_name varchar(30) not null,
	foreign key (department_name) references departments(name) on delete cascade,
	primary key (faculty_ID, department_name)
);


create table degree_programs(
	name varchar(30) unique not null,
	primary key (name),
	acronym char(4) not null unique,
	director char(5) not null,
	foreign key (director) references faculty(ID) on delete cascade,
	department varchar(30) not null,
	foreign key (department) references departments(name) on delete cascade,
	required_credits int(3) not null,
	required_courses int(2) not null
);


create table courses(
	acronym char(4) not null,
	num int(3) not null,
	primary key (acronym, num),
	title varchar(50) not null,
	description varchar(500) not null,
	program_name varchar(30) not null,
	foreign key (program_name) references degree_programs(name) on delete cascade
);


create table prerequisites(
	prereq_acronym char(4) not null,
	prereq_num int(3) not null,
	foreign key (prereq_acronym, prereq_num) references courses(acronym, num) on delete cascade,
	course_acronym char(4) not null,
	course_num int(3) not null,
	foreign key (course_acronym, course_num) references courses(acronym, num) on delete cascade,
	primary key (prereq_acronym, prereq_num, course_acronym, course_num),
	min_grade enum('A', 'B', 'C', 'D', 'F')
);


create table coursework_requirements(
	program_name varchar(30) not null,
	foreign key (program_name) references degree_programs(name) on delete cascade,
	course_acronym char(4) not null,
	course_num int(3) not null,
	foreign key (course_acronym, course_num) references courses(acronym, num) on delete cascade,
	primary key (program_name, course_acronym, course_num),
	reusable enum('yes', 'no') not null,
	min_grade enum('A', 'B', 'C', 'D', 'F')
);


create table course_offerings(
	course_acronym char(4) not null,
	course_num int(3) not null,
	foreign key (course_acronym, course_num) references courses(acronym, num) on delete cascade,
	section_num int(1) not null,
	semester_offered enum('spring', 'fall', 'winter', 'summer') not null,
	year_offered year not null,
	primary key (course_acronym, course_num, section_num, semester_offered, year_offered),
	teacher char(5) not null,
	foreign key (teacher) references faculty(ID) on delete cascade
);


create table meeting_periods(
	course_acronym char(4) not null,
	course_num int(3) not null,
	foreign key (course_acronym, course_num) references courses(acronym, num) on delete cascade,
	section_num int(1) not null,
	semester_offered enum('spring', 'fall', 'winter', 'summer') not null,
	year_offered year not null,
	weekday enum('M', 'T', 'W', 'R', 'F') not null,
	primary key (course_acronym, course_num, section_num, semester_offered, year_offered, weekday),
	time_start int(4) not null,
	time_finish int(4) not null,
	room_number int(3) not null,
	building_code char(4) not null
);


create table programs_pursuing(
	student_ID char(7) not null,
	foreign key (student_ID) references students(ID) on delete cascade,
	program_name varchar(30) not null,
	foreign key (program_name) references degree_programs(name) on delete cascade,
	primary key (student_ID, program_name),
	program_dropped enum('yes', 'no') not null
);


create table enrolled_courses(
	student_ID char(7) not null,
	foreign key (student_ID) references students(ID) on delete cascade,
	course_acronym char(4) not null,
	course_num int(3) not null,
	foreign key (course_acronym, course_num) references courses(acronym, num) on delete cascade,
	section_num int(1) not null,
	semester_offered enum('spring', 'fall', 'winter', 'summer') not null,
	year_offered year not null,
	primary key (student_ID, course_acronym, course_num, section_num, semester_offered, year_offered),
	grade_received enum('A', 'B', 'C', 'D', 'F', 'I', 'W', 'AU', 'NG')
);

	
create table student_degrees(
	student_ID char(7) not null,
	foreign key (student_ID) references students(ID) on delete cascade,
	degree_awarded varchar(30) not null unique,
	foreign key (degree_awarded) references degree_programs(name) on delete cascade,
	primary key (student_ID, degree_awarded),
	semester_awarded enum('spring', 'fall', 'winter', 'summer') not null,
	year_awarded year not null
);
	