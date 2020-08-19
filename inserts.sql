
insert into students values('0000000','Billy','Tables','m','1990-9-15','2015-5-7', 1.7, 2008, 'Squirreltown high school', 'maryland', '99999');
insert into students values('0000001','Jill','Lequeon','f','1992-1-1','2015-4-19', 4.3, 2010, 'Squirreltown high school', 'maryland', '99999');
insert into students values('0000002','Fred','McAllister','m','1970-3-28','2015-1-18', 3.5, 1988, 'Blackmeadow high school', 'maryland', '99819');
insert into students values('0000003','Mary','Woodshiner','f','1995-2-13','2016-5-7', 4.0, 2016, 'Riddletown high school', 'maryland', '99419');
insert into students values('0000004','Fanklin','Fiddlesticks','m','1995-7-1','2016-5-7', 3.7, 2016, 'Riddletown high school', 'maryland', '99419');
insert into students values('0000005','Rosie','Martinez','f','1994-11-11','2016-5-7', 3.85, 2016, 'Morrowville high school', 'maryland', '96819');
insert into students values('0000006','Ranalf','Zod','m','1994-12-28','2016-5-7', 2.4, 2016, 'Windsor high school', 'maryland', '19819');
insert into students values('0000007','Charlette','O\'Conner','f','1993-3-24','2016-5-7', 2.8, 2016, 'Black Mountain high school', 'maryland', '15819');
insert into students values('0000008','Morgan','Milany','m','1993-9-5','2016-5-7', 3.0, 2016, 'Red herring high school', 'ohio', '62319');
insert into students values('0000009','Ryan','O\'Brien','m','1994-5-7','2016-5-7', 3.1, 2016, 'Blue oyster high school', 'california', '91819');
insert into students values('0000010','Georgie','Jones','f','1995-6-13','2016-5-7', 3.5, 2016, 'Birchberry high school', 'virginia', '90219');


insert into faculty values('00000', 'Jeff', 'Smithee', 'jsmithee@gmail.com', '4105551010', 'professor', 'full-time', 'tenure-track', 'phd', 'computer science');
insert into faculty values('00001', 'Casandra', 'Robertson', 'casrob@gmail.com', '4105551011', 'instructor', 'part-time', 'non-tenure-track', 'bachelor', 'art');
insert into faculty values('00002', 'Veronica', 'Monica', 'veronimon@gmail.com', '4105551012', 'lecturer', 'full-time', 'adjunct', 'master', 'european history');
insert into faculty values('00003', 'Ed', 'Bloomensfeld', 'edblooom@gmail.com', '4105551013', 'assistant professor', 'full-time', 'tenure-track', 'phd', 'art');
insert into faculty values('00004', 'Jeff', 'Smithee', 'jsmithee@gmail.com', '4105551014', 'associate professor', 'full-time', 'tenure-track', 'phd', 'history');


insert into departments values('computer science', '00000', 107, 'shmn', '4105555555');
insert into departments values('art', '00003', 107, 'pahb', '4105555556');
insert into departments values('history', '00004', 208, 'shmn', '4105555557');


insert into faculty_departments values('00000', 'computer science');
insert into faculty_departments values('00001', 'computer science');
insert into faculty_departments values('00001', 'art');
insert into faculty_departments values('00001', 'history');
insert into faculty_departments values('00002', 'history');
insert into faculty_departments values('00003', 'art');
insert into faculty_departments values('00004', 'history');


insert into degree_programs values('computer science', 'cmsc', '00000', 'computer science', 9, 3);
insert into degree_programs values('art studies', 'arts', '00003', 'art', 6, 2);
insert into degree_programs values('european history', 'euhs', '00004', 'history', 6, 2);
insert into degree_programs values('american history', 'amhs', '00004', 'history', 6, 2);


insert into courses values('cmsc', 100, 'intro to computer science', 'teach the basics', 'computer science');
insert into courses values('cmsc', 101, 'intro to computer science II', 'teach some more basics', 'computer science');
insert into courses values('cmsc', 201, 'independent study', 'learn on your own. repeatable for credit.', 'computer science');
insert into courses values('arts', 100, 'finger painting', 'learn how to finger paint', 'art studies');
insert into courses values('euhs', 100, 'early european history', 'learn about europe', 'european history');


insert into prerequisites values('cmsc', 100, 'cmsc', 101, 'B');
insert into prerequisites values('cmsc', 100, 'cmsc', 201, 'B');
insert into prerequisites values('cmsc', 101, 'cmsc', 201, 'B');


insert into coursework_requirements values('computer science', 'cmsc', 100, 'no', 'B');
insert into coursework_requirements values('computer science', 'cmsc', 101, 'no', 'B');
insert into coursework_requirements values('computer science', 'cmsc', 201, 'yes', 'C');
insert into coursework_requirements values('art studies', 'arts', 100, 'no', 'B');
insert into coursework_requirements values('european history', 'euhs', 100, 'no', 'B');


insert into course_offerings values('cmsc', 100, 1, 'fall', 2016, '00000');
insert into course_offerings values('cmsc', 100, 2, 'fall', 2016, '00000');
insert into course_offerings values('cmsc', 100, 3, 'fall', 2016, '00001');
insert into course_offerings values('cmsc', 101, 1, 'fall', 2016, '00000');
insert into course_offerings values('cmsc', 101, 2, 'fall', 2016, '00000');
insert into course_offerings values('arts', 100, 1, 'fall', 2016, '00001');
insert into course_offerings values('arts', 100, 2, 'fall', 2016, '00003');
insert into course_offerings values('euhs', 100, 1, 'fall', 2016, '00001');
insert into course_offerings values('euhs', 100, 2, 'fall', 2016, '00002');
insert into course_offerings values('euhs', 100, 3, 'fall', 2016, '00004');


insert into meeting_periods values('cmsc', 100, 1, 'fall', 2016, 'M', 1300, 1415, 110, 'shmn');
insert into meeting_periods values('cmsc', 100, 1, 'fall', 2016, 'W', 1300, 1415, 110, 'shmn');
insert into meeting_periods values('cmsc', 100, 2, 'fall', 2016, 'M', 1430, 1545, 110, 'shmn');
insert into meeting_periods values('cmsc', 100, 2, 'fall', 2016, 'W', 1430, 1545, 110, 'shmn');
insert into meeting_periods values('cmsc', 100, 3, 'fall', 2016, 'M', 1500, 1800, 305, 'pahb');
insert into meeting_periods values('cmsc', 101, 1, 'fall', 2016, 'M', 1600, 1715, 110, 'shmn');
insert into meeting_periods values('cmsc', 101, 1, 'fall', 2016, 'W', 1600, 1715, 110, 'shmn');
insert into meeting_periods values('cmsc', 101, 2, 'fall', 2016, 'M', 1730, 1845, 110, 'shmn');
insert into meeting_periods values('cmsc', 101, 2, 'fall', 2016, 'W', 1730, 1845, 110, 'shmn');
insert into meeting_periods values('arts', 100, 1, 'fall', 2016, 'W', 1500, 1800, 305, 'pahb');
insert into meeting_periods values('arts', 100, 2, 'fall', 2016, 'T', 1200, 1500, 325, 'pahb');
insert into meeting_periods values('euhs', 100, 1, 'fall', 2016, 'M', 1200, 1500, 200, 'math');
insert into meeting_periods values('euhs', 100, 2, 'fall', 2016, 'M', 1500, 1800, 205, 'math');
insert into meeting_periods values('euhs', 100, 3, 'fall', 2016, 'M', 1200, 1250, 127, 'math');
insert into meeting_periods values('euhs', 100, 3, 'fall', 2016, 'W', 1200, 1250, 127, 'math');
insert into meeting_periods values('euhs', 100, 3, 'fall', 2016, 'F', 1200, 1250, 127, 'math');


insert into programs_pursuing values ('0000000', 'computer science', 'no');
insert into programs_pursuing values ('0000000', 'art studies', 'no');
insert into programs_pursuing values ('0000000', 'european history', 'yes');
insert into programs_pursuing values ('0000001', 'art studies', 'no');
insert into programs_pursuing values ('0000002', 'computer science', 'no');
insert into programs_pursuing values ('0000003', 'european history', 'no');
insert into programs_pursuing values ('0000004', 'computer science', 'no');
insert into programs_pursuing values ('0000005', 'computer science', 'no');
insert into programs_pursuing values ('0000006', 'art studies', 'no');
insert into programs_pursuing values ('0000007', 'european history', 'no');
insert into programs_pursuing values ('0000008', 'computer science', 'no');
insert into programs_pursuing values ('0000009', 'art studies', 'no');
insert into programs_pursuing values ('0000010', 'art studies', 'no');


insert into enrolled_courses values ('0000000', 'cmsc', 101, 1, 'fall', 2016, null);
insert into enrolled_courses values ('0000000', 'euhs', 100, 1, 'fall', 2016, 'W');
insert into enrolled_courses values ('0000000', 'cmsc', 100, 1, 'spring', 2016, 'A');
insert into enrolled_courses values ('0000000', 'cmsc', 100, 1, 'fall', 2015, 'D');
insert into enrolled_courses values ('0000001', 'arts', 100, 1, 'fall', 2015, 'A');
insert into enrolled_courses values ('0000001', 'cmsc', 100, 1, 'fall', 2015, 'B');
insert into enrolled_courses values ('0000001', 'arts', 100, 1, 'fall', 2016, null);
insert into enrolled_courses values ('0000002', 'euhs', 100, 1, 'fall', 2016, null);
insert into enrolled_courses values ('0000002', 'cmsc', 201, 5, 'fall', 2015, 'A');
insert into enrolled_courses values ('0000002', 'cmsc', 101, 6, 'fall', 2015, 'A');
insert into enrolled_courses values ('0000002', 'cmsc', 100, 1, 'spring', 2015, 'A');
insert into enrolled_courses values ('0000002', 'arts', 100, 1, 'spring', 2015, 'A');


insert into student_degrees values ('0000002', 'computer science', 'spring', 2016);
insert into student_degrees values ('0000002', 'art studies', 'spring', 2016);

