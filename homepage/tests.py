import pytest
from homepage.models import Course, Review, Professor, Professor_to_Course, Prerequisites
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import QuerySet
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
    date1 = datetime(2015, 10, 9, 23, 55, 59, 5, tzinfo=pytz.UTC)
    date2 = datetime(2016, 10, 9, 23, 55, 59, 5, tzinfo=pytz.UTC)
    date3 = datetime(2015, 10, 3, 20, 00, 3, 5, tzinfo=pytz.UTC)
    date4 = datetime(2017, 3, 9, 18, 20, 00, 5, tzinfo=pytz.UTC)
    date5 = datetime(2016, 5, 2, 7, 00, 00, 5, tzinfo=pytz.UTC)
    date6 = datetime(2015, 6, 1, 12, 20, 00, 5, tzinfo=pytz.UTC)
    image = 'images/new_test_image.jpg'

    assert reviews_list == [
        (10111, 1, 5, date1, 'Great course', 3, 3, image),
        (10111, 1, 4, date2, "I've learned a lot!", 2, None, ''),
        (10221, 2, 4, date3, 'The course was difficult', 5, 1, ''),
        (10221, 2, 3, date4, "I didn't learn anything new", 3, None, ''),
        (10231, 3, 4, date5, 'This course helped me to find a job', 2, None, ''),
        (10231, 3, 3, date6, "I didn't understand the material", 4, None, ''),
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


@pytest.mark.django_db
def test_main_feed():
    result = Review.main_feed()
    assert isinstance(result, QuerySet)
    assert all(isinstance(review, Review) for review in result)
    ids_list = list(result.values_list('id'))
    assert [arg[0] for arg in ids_list] == [4, 2, 5, 1, 3, 6]

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


# ---------Professor tests----------#

@pytest.fixture
def professors_list():
    return list(Professor.objects.values_list('name'))


@pytest.fixture
def valid_name():
    return 'Severus Snape'


@pytest.fixture
def invalid_name():
    return 'Pablo Diego Jose Francisco de Paula Juan Nepomuceno Maria de \
    los Remedios Cipriano de la Santisima Trinidad Ruiz y Picasso Snape'


# check the data stored in database from 0004_professor_test_data.py file
@pytest.mark.django_db
def test_model_professors_list(professors_list):

    assert professors_list == [
        ('Septima Vector',),
        ('Sybill Patricia Trelawney',),
        ('Bathsheda Babbling',),
    ]


@pytest.mark.django_db
def test_add_valid_professor(valid_name):
    professor = Professor(name=valid_name)
    professor.save()

    created_professor = Professor.objects.get(pk=professor.id)
    assert created_professor.name == valid_name


# name is too long (>100)
@pytest.mark.django_db
def test_create_invalid_professor(invalid_name):
    invalid = False
    try:
        Professor(invalid_name).clean_fields()
    except ValidationError:
        invalid = True

    assert invalid


@pytest.mark.django_db
def test_professor_str(valid_name):
    professor = Professor(name=valid_name)

    assert str(professor) == professor.name


# -----Professor to course tests-----#

@pytest.fixture
def professor_to_course_list():
    return list(Professor_to_Course.objects.values_list(
        'professor_id', 'course_id'))


# check the data stored in database from 0004_professor_test_data.py file
@pytest.mark.django_db
def test_professor_to_course_list(professor_to_course_list):

    assert professor_to_course_list == [
        (1, 10221),
        (1, 12357),
        (2, 10231),
        (3, 10111)
    ]


@pytest.mark.django_db
def test_add_valid_pro_to_course():
    relation = Professor_to_Course(
        professor_id=Professor.objects.get(pk=2),
        course_id=Course.objects.get(pk=10231)
    )
    relation.save()

    assert Professor_to_Course.objects.filter(pk=relation.id).exists()


# course does not exist (wrong id)
@pytest.mark.django_db
def test_add_invalid_course():
    invalid = False

    try:
        Professor_to_Course(
            Professor.objects.get(pk=2),
            Course.objects.get(pk=10233)
        ).clean_fields()
    except ObjectDoesNotExist:
        invalid = True

    assert invalid


# professor does not exist (wrong id)
@pytest.mark.django_db
def test_add_invalid_professor():
    invalid = False

    try:
        Professor_to_Course(
            Professor.objects.get(pk=5),
            Course.objects.get(pk=10231)).clean_fields()
    except ObjectDoesNotExist:
        invalid = True

    assert invalid


@pytest.mark.django_db
def test_get_pro_by_course():
    professors = Professor_to_Course.get_professors_by_course(
        Course.objects.get(pk=10231)
    )

    assert (len(professors) == 1) and (Professor.objects.get(pk=2) in professors)


@pytest.mark.django_db
def test_get_course_by_pro():
    courses = Professor_to_Course.get_courses_by_professor(
        Professor.objects.get(pk=1)
    )

    course1 = Course.objects.get(pk=10221)
    course2 = Course.objects.get(pk=12357)
    assert (len(courses) == 2) and (course1 in courses) and (course2 in courses)


@pytest.mark.django_db
def test_pro_to_course_str():
    relation = Professor_to_Course.objects.get(pk=1)

    assert str(relation) == 'professor = Septima Vector, course_id = 10221'
