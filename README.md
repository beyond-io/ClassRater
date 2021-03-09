# ClassRater

ClassRater is a course information and rating application, focused on MTA courses.

It is a solution to a well known problem: the course syllabi available don't give sufficient information to aspiring students, and so the students struggle with creating an appropriate schedule for themselves.

The previous solution is a facebook page, dedicated to this purpose, but it is difficult to search and lacks centralized information.

ClassRater improves on this situation by introducing an easy to use data structure, which defaults to a centralized experience: no redundancies, no duplicates, all related information is found in one place.

Using it, students can search for specific courses, read reviews written by other students, and make more informed decisions.

## Features

* Display of all available courses in table format 

* Sort by:
	* course identifier code
	* course name
	* rating
	* number of reviews

* Complex Search by:
	* course identifier code
	* course name
	* rating
	* number of reviews
	* Elective \ Mandatory
	* Program
	* Year in Program
		
* Filter by:
	* Electives
	* Mandatories
	* Programs
	* Year in Program
	* Semester availability
	* Prerequisites 
	* Course star rating
	* Course time demand
	* Course difficulty
	* Number of raters
	* Number of reviews

* Add Review / Rating

## Technologies:

ClassRater uses:
* Virtualization:
	* [Vagrant](https://www.vagrantup.com/)
	* [Oracle VM VirtualBox](https://www.virtualbox.org/)
* Requirements Management:
	* [pipenv](https://pypi.org/project/pipenv/)
* Application:
	* [python](https://www.python.org/)
	* [Django](https://www.djangoproject.com/)
	* [SQLite](https://www.sqlite.org/index.html)
* Templating:
	* HTML5
	* scss
	* [Bootstrap](https://getbootstrap.com/)
* Automatic Python Syntax Testing:
	* [flake8](https://flake8.pycqa.org/en/latest/)

## Members:

Ori Adler, 
Yair Dana, 
Leon Rabinovich, 
Vera Tsvang, 
Ella Milyavsky

