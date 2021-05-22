# ClassRater

ClassRater is a course information and rating application, focused on MTA courses.

It is a solution to a well known problem: the course syllabi available don't give sufficient information to aspiring students, and so the students struggle with creating an appropriate schedule for themselves.

The previous solution is a facebook page, dedicated to this purpose, but it is difficult to search and lacks centralized information.

ClassRater improves on this situation by introducing an easy to use data structure, which defaults to a centralized experience: no redundancies, no duplicates, all related information is found in one place.

Using ClassRater, students can search for specific courses, read reviews written by other students, and make more informed decisions.

## Features

* Display of all available courses in table format 

* Sort by:
	* course identifier code
	* course name
	* course rating
	* course load
	* number of raters
	* number of reviews

* Search by course name
* Filter by:
	* Electives
	* Mandatories
	* Prerequisites 
	* Course rating
	* Course load
	* Number of raters
	* Number of reviews

* Add Review / Rating: 
	* with or without referencing professor

## Technologies Used:

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
	* [pillow] (https://pillow.readthedocs.io/en/stable/)
* Templating:
	* HTML5
	* scss
	* [Bootstrap](https://getbootstrap.com/)
	* [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/)
* Automatic Python Syntax Testing:
	* [flake8](https://flake8.pycqa.org/en/latest/)
* Automated testing:
	* [pytest](https://docs.pytest.org/en/6.2.x/)
	* [pytest-django](https://pytest-django.readthedocs.io/en/latest/)

## Members:

Ori Adler, 
Leon Rabinovich, 
Vera Tsvang, 
Ella Milyavsky

