import pytest
from homepage.models import Course, Review, Prerequisites
from django.core.exceptions import ValidationError
from datetime import datetime
import pytz


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


# -----------Review tests----------- #
@pytest.fixture
def reviews_list():
    return list(Review.objects.values_list(
        'course', 'user', 'rate', 'date', 'content', 'course_load', 'professor', 'image'))


# check the data stored in database from 0006_review_test_data.py file
@pytest.mark.django_db
def test_model_review_list(reviews_list):
    cur_date = datetime(2015, 10, 9, 23, 55, 59, 5, tzinfo=pytz.UTC)
    image = 'images/new_test_image.jpg'

    assert reviews_list == [
        (10111, 1, 5, cur_date, 'Great course', 3, 3, image),
        (10111, 1, 4, cur_date, "I've learned a lot!", 2, None, ''),
        (10221, 2, 4, cur_date, 'The course was difficult', 5, 1, ''),
        (10221, 2, 3, cur_date, "I didn't learn anything new", 3, None, ''),
        (10231, 3, 4, cur_date, 'This course helped me to find a job', 2, None, ''),
        (10231, 3, 3, cur_date, "I didn't understand the material", 4, None, ''),
    ]


@pytest.mark.parametrize("valid_review", [
    (10, 10231, 3, 3, datetime(2017, 9, 8, 22, 55, 59, 5, tzinfo=pytz.UTC), "It was too difficult", 4, 0, None, ''),
    (11, 10111, 2, 4, datetime(2017, 9, 8, 22, 55, 59, 5, tzinfo=pytz.UTC), "I've learned a lot!", 4, 0, None, ''),
])
@pytest.mark.django_db
def test_add_valid_review(valid_review):
    review = Review(*valid_review)
    review.save()

    assert Review.objects.filter(pk=review.id).exists()


@pytest.mark.parametrize("invalid_review", [
    (10, 10231, 3, 10, datetime(2015, 10, 9, 23, 55, 59, 5, tzinfo=pytz.UTC), "Great course!", 4, 0, None, ''),
    # 0: rate > 5  ^rate
    (11, 10111, 2, 4, datetime(2017, 9, 8, 22, 55, 59, 5, tzinfo=pytz.UTC), "I've learned a lot!", 0, 0, None, ''),
    # 2: course_load < 1                                                                           ^course_load
])
@pytest.mark.django_db
def test_create_invalid_review(invalid_review):
    invalid = False

    try:
        Review(*invalid_review).clean_fields()
    except ValidationError:
        invalid = True

    assert invalid


@pytest.mark.parametrize("new_review, expected_string", [
    ((10, 10231, 3, 3, datetime(2015, 10, 9, 23, 55, 59, 5, tzinfo=pytz.UTC),
        "I didn't understand the material at all?!", 4, 0, None, ''),
        "Shortened review: I didn't understand the material..."),
    ((11, 10111, 2, 4, datetime(2017, 9, 8, 22, 55, 59, 5, tzinfo=pytz.UTC),
        "I've learned a lot, helped me to find a job", 4, 0, None, ''),
        "Shortened review: I've learned a lot, helped..."),
])
def test_review_str(new_review, expected_string):
    review = Review(*new_review)

    assert str(review) == expected_string


@pytest.mark.parametrize("review_id, expected_review_details", [
    (1, "Course: Resonance in Runes and Signs\n" + "User: testUser1\n" + "Rating: 5\n" +
        "Shortened review: Great course...\n" + "Course load: 3\n" +
        "Likes number: 10\n" + "Professor: Bathsheda Babbling\n"),
    # 2-Course: check a review without professor returns 'N/A'
    (2, "Course: Resonance in Runes and Signs\n" + "User: testUser1\n" + "Rating: 4\n" +
        "Shortened review: I've learned a lot!...\n" + "Course load: 2\n" +
        "Likes number: 4\n" + "Professor: N/A\n"),
    (3, "Course: Grammatica in Arithmancy\n" + "User: testUser2\n" + "Rating: 4\n" +
        "Shortened review: The course was difficult...\n" + "Course load: 5\n" +
        "Likes number: 0\n" + "Professor: Septima Vector\n"),
])
@pytest.mark.django_db
def test_print_details(capsys, review_id, expected_review_details):
    Review.objects.get(pk=review_id).print_details()

    assert capsys.readouterr().out == expected_review_details

# -----------prerequisites tests----------- #


# three courses:
@pytest.fixture
def courses():
    courses_list = [
         Course(1, "Course1", True, 3, "N/A", 1.3, 4, 5, 1),
         Course(2, "Course2", False, 2, "N/A", 3.5, 2, 13, 5),
         Course(3, "Course3", False, 1, "N/A", 2, 2.5, 0, 0)
         ]
    for course in courses_list:
        course.save()

    return courses_list


@pytest.fixture
def preqs_list(courses):
    return [Prerequisites(course_id=courses[1], req_course_id=courses[0], req_code=Prerequisites.Req_Code.BEFORE),
            Prerequisites(course_id=courses[1], req_course_id=courses[2], req_code=Prerequisites.Req_Code.BEFORE)]


# creating a new prerequisite log
@pytest.mark.django_db
def test_create_new_prerequisite(courses, preqs_list):
    valid = True
    preq = preqs_list[0]
    try:
        preq.clean_fields()
        preq.save()
    except ValidationError:
        valid = False

    assert valid and Prerequisites.objects.filter(course_id=preq.course_id).count() == 1


# creating a new invalid prerequisite log - req_code invalid
@pytest.mark.django_db
def test_create_new_invalid_prerequisite(courses):
    invalid = False
    preq = Prerequisites(course_id=courses[1], req_course_id=courses[0], req_code=3)
    try:
        preq.clean_fields()
    except ValidationError:
        invalid = True

    assert invalid


@pytest.mark.django_db
def test_prerequisite_print(courses, preqs_list, capsys):
    preq = preqs_list[0]
    preq.save()

    msg = f"Req. Course = Course1, Desired Course = Course2, Req. Code = {Prerequisites.Req_Code.BEFORE}\n"
    print(preq)
    assert capsys.readouterr().out == msg


@pytest.mark.django_db
# test for Course2 which has prerequisite - Course1
def test_get_prerequisites_for_course_with_one_preqs(courses, preqs_list):
    preq = preqs_list[0]
    preq.save()

    assert Prerequisites.get_prerequisites_for_course(courses[1]).count() == 1


@pytest.mark.django_db
# test for Course2 which here depends on taking Course1 and Course3 both
def test_get_prerequisites_for_course_with_multi_preqs(courses, preqs_list):
    for preq in preqs_list:
        preq.save()

    assert Prerequisites.get_prerequisites_for_course(courses[1]).count() == 2


@pytest.mark.django_db
# Course1 has no prerequisites
def test_get_prerequisites_for_course_with_no_preqs(courses):

    assert not Prerequisites.get_prerequisites_for_course(courses[0]).exists()


@pytest.mark.django_db
# test to see it returns True
def test_does_course_have_prerequisites_one_preqs(courses, preqs_list):
    preq = preqs_list[0]
    preq.save()

    assert Prerequisites.does_course_have_prerequisites(courses[1])


@pytest.mark.django_db
# test to see it returns True
def test_does_course_have_prerequisites_for_multi_preqs(courses, preqs_list):
    for preq in preqs_list:
        preq.save()

    assert Prerequisites.does_course_have_prerequisites(courses[1])


@pytest.mark.django_db
# Course1 has no prerequisites - test to see it returns False
def test_does_course_have_prerequisites_for_no_preqs(courses):

    assert not Prerequisites.does_course_have_prerequisites(courses[0])
