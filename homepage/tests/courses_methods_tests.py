import pytest
from homepage.models import Course
from django.core.exceptions import ValidationError
from decimal import Decimal

# -----------course tests----------- #


# creating a single new course with valid input
@pytest.mark.parametrize("valid_courses", [
    (1, "Linear Algebra 1", True, 4),
    #                               ^- no input at all for syllabi onwards
    (1, "Linear Algebra 1", True, 4, None),
    #                                    ^- no input at all for avg_rating onwards
    (1, "Linear Algebra 1", True, 4, "https://www.google.com"),
    #                                  ^- available syllabus
    (1, "Linear Algebra 1", True, 4, None, 3.5, 4, 13, 7),
    #                                                   ^- complete with all course fields
    ])
@pytest.mark.django_db
def test_course_validation_valids(valid_courses):
    flag = True

    # check that valid input doesn't raise exception
    try:
        Course(*valid_courses).clean_fields()
    except ValidationError:
        flag = False

    assert flag


@pytest.mark.parametrize("valid_courses", [
    (1, "Linear Algebra 1", True, 4),
    #                               ^- no input at all for syllabi onwards
    (1, "Linear Algebra 1", True, 4, None),
    #                                    ^- no input at all for avg_rating onwards
    (1, "Linear Algebra 1", True, 4, "https://www.google.com"),
    #                                  ^- available syllabus
    (1, "Linear Algebra 1", True, 4, None, 3.5, 4, 13, 7),
    #                                                   ^- complete with all course fields
    ])
@pytest.mark.django_db
def test_course_save_course(valid_courses):
    course = Course(*valid_courses)
    course.save()
    # check that it's the same object
    db_course = Course.objects.get(pk=course.course_id)
    assert db_course == course


@pytest.mark.parametrize("invalid_courses", [
    (-1, "Linear Algebra 1", True, 4, None, 3.5, 4, 13, 7),
    # ^- id < 0
    (1, "Linear Algebra 1", True, 0, None, 3.5, 4, 13, 7),
    #                             ^- credit points less than 1
    (1, "Linear Algebra 1", True, 1000, None, 3.5, 4, 13, 7),
    #                             ^- credit points too big
    (1, "Linear Algebra 1", True, 4, "I am not a url", 3.5, 4, 13, 7),
    #                                 ^- not a url
    (1, "Linear Algebra 1", True, 4, None, 0, 4, 13, 7),
    #                                      ^- avg course load less than 1
    (1, "Linear Algebra 1", True, 4, None, 7, 4, 13, 7),
    #                                      ^- avg course load more than 5
    (1, "Linear Algebra 1", True, 4, None, 3.5, 0, 13, 7),
    #                                           ^- avg course rating less than 1
    (1, "Linear Algebra 1", True, 4, None, 3.5, 7, 13, 7),
    #                                           ^- avg course rating more than 5
    (1, "Linear Algebra 1", True, 4, None, 3.5, 4, -1, 7),
    #                                               ^- number of rater less than 0
    (1, "Linear Algebra 1", True, 4, None, 3.5, 4, 13, -1),
    #                                                   ^- number of reviewers less than 0
    (1, "Linear Algebra 1", True, 4, None, 3.5, None, 5),
    #                                       ^- avg_load without avg_rating
    (1, "Linear Algebra 1", True, 4, None, None, 4, 10),
    #                                             ^- avg_rating without avg_load
    (1, "Linear Algebra 1", True, 4, None, None, None, 2),
    #                                                   ^- no ratings but raters num is > 0
    (1, "Linear Algebra 1", True, 4, None, 3.5, 4),
    #                                            ^- rating reviews without rater numbers
    (1, "Linear Algebra 1", True, 4, None, None, None, 0, 13),
    #                                                      ^- reviewes without rating reviews
    ])
@pytest.mark.django_db
def test_course_validation_invalids(invalid_courses):
    flag = False

    try:
        Course(*invalid_courses).full_clean()
    except ValidationError:
        flag = True

    assert flag


@pytest.mark.parametrize("invalid_courses", [
    (1, "Linear Algebra 1", True, 4, None, 3.5, None, 5),
    #                                       ^- avg_load without avg_rating
    (1, "Linear Algebra 1", True, 4, None, None, 4, 10),
    #                                             ^- avg_rating without avg_load
    (1, "Linear Algebra 1", True, 4, None, None, None, 2),
    #                                                   ^- no ratings but raters num is > 0
    (1, "Linear Algebra 1", True, 4, None, 3.5, 4),
    #                                            ^- rating reviews without rater numbers
    (1, "Linear Algebra 1", True, 4, None, None, None, 0, 13),
    #                                                      ^- reviewes without rating reviews
    ])
@pytest.mark.django_db
def test_invalid_course_creation(invalid_courses):
    course = Course(*invalid_courses)
    course.save()

    assert Course.objects.filter(pk=course.course_id).count() == 0


# test the print_details function
@pytest.mark.django_db
def test_course_print_details(capsys):
    course = (1, "Linear Algebra 1", True, 4, None, 3.500, 4.000, 13, 7)
    Course(*course).save()

    msg = (
        "------------------------------------------------------------\n"
        "Course indentifier: 1   \nName: Linear Algebra 1\nMandatory? yes\n"
        "Credit Points: 4\nSyllabi: N/A\n"
        "Average Rating: 4.000 \tAverage Load: 3.500\t"
        "13 Raters\nNumber Of Reviews: 7\n"
        )
    # make sure that message comes out as expected
    Course.objects.get(pk=1).print_details()
    assert capsys.readouterr().out == msg


# test the print_details function
@pytest.mark.django_db
def test_course_print_details_without_ratings(capsys):
    course = Course.objects.get(pk=10340)

    msg = (
        "------------------------------------------------------------\n"
        "Course indentifier: 10340   \nName: No Return - through the Lense\nMandatory? yes\n"
        "Credit Points: 4\nSyllabi: N/A\n"
        "Average Rating: N/A \tAverage Load: N/A\t"
        "0 Raters\nNumber Of Reviews: 0\n"
        )
    # make sure that message comes out as expected
    course.print_details()
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


@pytest.fixture
def courses():
    courses_list = [
         Course(1, "Course1", True, 3, None),
         Course(2, "Course2", False, 2, None, 3.5, 2, 13, 5),
         Course(3, "Course3", False, 1, None, 3.5, 2, 13, 0)
         ]
    for course in courses_list:
        course.save()

    return courses_list


# updating courses after review
@pytest.mark.django_db
def test_update_course_with_previous_data(courses):
    # testing on Course2
    course = courses[1]
    course.update_course_per_review(3, 1, False)  # simulates review that gave rating: 3 load: 1 and no text review
    db_course = Course.objects.get(pk=course.course_id)
    # expect rating to be (3 + 2*13) / 14 = 2.07142

    assert db_course.avg_rating.compare(Decimal('2.07143')) == 0    # assert change
    assert db_course.avg_load.compare(Decimal('3.32143')) == 0      # assert change
    assert db_course.num_of_raters == 14                            # assert change
    assert db_course.num_of_reviewers == 5                          # assert no change


@pytest.mark.django_db
def test_update_course_with_partial_previous_data(courses):
    # testing on Course3
    course = courses[2]
    course.update_course_per_review(3, 1, True)    # simulates review that gave rating: 3 load: 1 and no text review
    db_course = Course.objects.get(pk=course.course_id)
    # expect rating to be (3 + 2*13) / 14 = 2.07142

    assert db_course.avg_rating.compare(Decimal('2.07143')) == 0    # assert change
    assert db_course.avg_load.compare(Decimal('3.32143')) == 0      # assert change
    assert db_course.num_of_raters == 14                            # assert change
    assert db_course.num_of_reviewers == 1                          # assert change


@pytest.mark.django_db
def test_update_course_with_no_prev_data(courses):
    # testing for Course1
    course = courses[0]
    course.update_course_per_review(3, 1, True)    # simulates review that gave rating: 3 load: 1 and no text review
    db_course = Course.objects.get(pk=course.course_id)

    assert db_course.avg_rating.compare(Decimal('3.00000')) == 0    # assert change
    assert db_course.avg_load.compare(Decimal('1.00000')) == 0      # assert change
    assert db_course.num_of_raters == 1                             # assert change
    assert db_course.num_of_reviewers == 1                          # assert change
