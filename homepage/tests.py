import pytest
from homepage.models import Course
from django.core.exceptions import ValidationError


# -----------course tests----------- #
# creating a single new course with valid input
@pytest.mark.django_db
def test_course_create_course():
    id = 1
    name = "Linear Algebra 1"
    mandatory = True
    credit = 4
    syllabi = "please contribute"
    avg_load = 3.5
    avg_rating = 4
    num_raters = 13
    num_reviewers = 7
    flag = True

    # check that valid input doesn't raise exception
    try:
        Course(id, name, mandatory, credit, syllabi, avg_load, avg_rating, num_raters, num_reviewers).clean_fields()
    except ValidationError:
        flag = False

    assert flag

    course = Course(id, name, mandatory, credit, syllabi, avg_load, avg_rating, num_raters, num_reviewers)
    course.save()
    # check that it's the same object
    db_course = Course.objects.get(pk=id)
    assert db_course == course


@pytest.mark.parametrize("invalid_courses", [
    (-1, "Linear Algebra 1", True, 4, "please contribute", 3.5, 4, 13, 7),
    # ^- id < 0
    (1, "Linear Algebra 1", True, 0, "please contribute", 3.5, 4, 13, 7),
    #                             ^- credit points less than 1
    (1, "Linear Algebra 1", True, 1000, "please contribute", 3.5, 4, 13, 7),
    #                             ^- credit points too big
    (1, "Linear Algebra 1", True, 4, "please contribute", 0, 4, 13, 7),
    #                                                     ^- avg course load less than 1
    (1, "Linear Algebra 1", True, 4, "please contribute", 7, 4, 13, 7),
    #                                                     ^- avg course load more than 5
    (1, "Linear Algebra 1", True, 4, "please contribute", 3.5, 0, 13, 7),
    #                                                           ^- avg course rating less than 1
    (1, "Linear Algebra 1", True, 4, "please contribute", 3.5, 7, 13, 7),
    #                                                           ^- avg course rating more than 5
    (1, "Linear Algebra 1", True, 4, "please contribute", 3.5, 4, -1, 7),
    #                                                              ^- number of rater less than 0
    (1, "Linear Algebra 1", True, 4, "please contribute", 3.5, 4, 13, -1),
    #                                                                  ^- number of reviewers less than 0
    ])
@pytest.mark.django_db
def test_course_create_invalid_course(invalid_courses):
    flag = False

    try:
        Course(*invalid_courses).clean_fields()
    except ValidationError:
        flag = True

    assert flag


# test the print_details function
@pytest.mark.django_db
def test_course_print_details(capsys):
    course = (1, "Linear Algebra 1", True, 4, "please contribute", 3.500, 4.000, 13, 7)
    Course(*course).save()

    msg = (
        "------------------------------------------------------------\n"
        "Course indentifier: 1   \nName: Linear Algebra 1\nMandatory? yes\n"
        "Credit Points: 4\nSyllabi: please contribute\n"
        "Average Rating: 4.000 \tAverage Load: 3.500\t"
        "13 Raters\nNumber Of Reviews: 7\n"
        )
    # make sure that message comes out as expected
    Course.objects.get(pk=1).print_details()
    assert capsys.readouterr().out == msg


# test the get_details function
@pytest.mark.django_db
def test_course_get_details():
    course = (1, "Linear Algebra 1", True, 4, "please contribute", 3.500, 4.000, 13, 7)
    Course(*course).save()
    # make sure details are saved accurately
    assert Course.objects.get(pk=course[0]).get_details() == course


# creating multiple new courses
@pytest.mark.django_db
def test_create_multiple_courses():
    details = [(1, "Linear Algebra 1", True, 4, "please contribute", 3.5, 4, 13, 7),
               (2, "Project Management", False, 3, "please contribute", 1.5, 3.5, 15, 3)]

    for args in details:
        Course(*args).save()
    # make sure that multiple courses are saved accurately
    courses = [Course.objects.get(pk=arg[0]).get_details() for arg in details]
    assert courses == details
