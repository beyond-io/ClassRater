import pytest
from homepage.models import Course, Prerequisites
from homepage.forms import FilterForm
from pytest_django.asserts import assertTemplateUsed


# --- testing the filtering functions:
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
    preqs = [Prerequisites(course_id=courses[1], req_course_id=courses[0], req_code=Prerequisites.Req_Code.BEFORE),
             Prerequisites(course_id=courses[1], req_course_id=courses[2], req_code=Prerequisites.Req_Code.BEFORE)]
    for preq in preqs:
        preq.save()
    return preqs


@pytest.fixture
def all_courses():
    return Course.objects.all()


# test that each of the new courses is returned with the method
@pytest.mark.django_db
def test_get_courses(courses):
    flag = True
    db_courses = Course.get_courses()
    for course in courses:
        flag = flag and db_courses.filter(pk=course.pk).exists()

    assert flag


# test the has_preqs method - if a course with preqs returns True and withuot returns False
@pytest.mark.django_db
def test_course_has_preqs(courses, preqs_list):
    has_preqs = []
    desired_res = [False, True, False]
    for course in courses:
        has_preqs.append(course.has_preqs())
    for ind in range(0, 2):
        assert has_preqs[ind] == desired_res[ind]

# -- testing single filter


@pytest.mark.django_db
def test_get_filtered_courses_by_rating(courses, all_courses):
    # testing for the average rating >= 2.5 which should include Course1 and Course3
    db_courses = Course.get_filtered_courses_by_rating(2.5, all_courses)

    assert db_courses.filter(pk=courses[0].course_id) and db_courses.filter(pk=courses[2].course_id)
    assert not db_courses.filter(pk=courses[1].course_id)


@pytest.mark.django_db
def test_get_filtered_courses_by_load(courses, all_courses):
    # testing for the average load <= 2 which should include Course1 and Course3
    db_courses = Course.get_filtered_courses_by_load(2, all_courses)

    assert db_courses.filter(pk=courses[0].course_id) and db_courses.filter(pk=courses[2].course_id)
    assert not db_courses.filter(pk=courses[1].course_id)


@pytest.mark.django_db
def test_get_mandatory_courses(courses, all_courses):
    # should get back only Course1 from courses
    db_courses = Course.get_mandatory_courses(all_courses)

    assert db_courses.filter(pk=courses[0].course_id)
    assert not db_courses.filter(pk=courses[1].course_id) and not db_courses.filter(pk=courses[2].course_id)


@pytest.mark.django_db
def test_get_elective_courses(courses, all_courses):
    # should get back only Course1 from courses
    db_courses = Course.get_elective_courses(all_courses)

    assert not db_courses.filter(pk=courses[0].course_id)
    assert db_courses.filter(pk=courses[1].course_id) and db_courses.filter(pk=courses[2].course_id)

# -- testing double filter


# test rating and mandatory filter
@pytest.mark.django_db
def test_rating_and_mandatory_filters(courses, all_courses):
    # expect to return only Course1
    db_courses = Course.get_filtered_courses_by_rating(2.5, all_courses)
    db_courses = Course.get_mandatory_courses(db_courses)

    assert db_courses.filter(pk=courses[0].course_id)
    assert not db_courses.filter(pk=courses[1].course_id) and not db_courses.filter(pk=courses[2].course_id)


# test rating and elective filter
@pytest.mark.django_db
def test_rating_and_elective_filters(courses, all_courses):
    # expect to return only Course3
    db_courses = Course.get_filtered_courses_by_rating(2.5, all_courses)
    db_courses = Course.get_elective_courses(db_courses)

    assert db_courses.filter(pk=courses[2].course_id)
    assert not db_courses.filter(pk=courses[1].course_id) and not db_courses.filter(pk=courses[0].course_id)


# test mandatory and elective filter - expect empty result
@pytest.mark.django_db
def test_elective_and_mandatory_filters(all_courses):
    # expect to return only Course1
    db_courses = Course.get_elective_courses(all_courses)
    db_courses = Course.get_mandatory_courses(db_courses)

    assert not db_courses


# test load and elective and mandatory filters
@pytest.mark.django_db
def test_load_and_elective_and_mandatory_filters(courses, all_courses):
    # expect to return only Course3
    db_courses = Course.get_filtered_courses_by_load(2, all_courses)
    db_courses_elect = Course.get_elective_courses(db_courses)
    db_courses_mand = Course.get_mandatory_courses(db_courses)

    # checking elective is only Course3
    assert db_courses_elect.filter(pk=courses[2].course_id)
    assert not db_courses_elect.filter(pk=courses[1].course_id) and not db_courses_elect.filter(pk=courses[0].course_id)

    # checking mandatory is only Course1
    assert db_courses_mand.filter(pk=courses[0].course_id)
    assert not db_courses_mand.filter(pk=courses[1].course_id) and not db_courses_mand.filter(pk=courses[2].course_id)


# test rating and load
@pytest.mark.django_db
def test_get_rating_and_load_filters(courses, all_courses):
    # expect only Course1
    db_courses = Course.get_filtered_courses_by_load(2, all_courses)
    db_courses = Course.get_filtered_courses_by_rating(3, db_courses)

    assert db_courses.filter(pk=courses[0].course_id)

# --- test the view and form --- #


# test that initial, no filter, QuerySet contains all courses from test_data
@pytest.mark.django_db
def test_with_client(client):
    courses = list(Course.get_courses().values_list('course_id'))
    response = client.get('/courses/')
    assert response.status_code == 200
    view_courses = list(response.context['all_courses'].values_list('course_id'))
    assert courses == view_courses


# test that the post response is the desired form model
@pytest.mark.django_db
def test_uses_filter_form(client):
    response = client.get('/courses/')
    assert isinstance(response.context['form'], FilterForm)


# test that the form model reacts to valid input
@pytest.mark.django_db
def test_post_valid_filter_with_client(all_courses, client):
    response = client.post('/courses/', data={'mand': 'mandatory'})
    assert response.status_code == 200


@pytest.mark.django_db
def test_renders_reviews_template(client):
    response = client.get('/courses/')

    assert response.status_code == 200
    assertTemplateUsed(response, 'homepage/courses/courses.html')
