import pytest
from homepage.models import Course
from django.db.models import QuerySet
from pytest_django.asserts import assertTemplateUsed


# --------Backend testing-------- #
@pytest.mark.django_db
def test_type_get_courses_ordered_by_name():
    # because an empty string is a substring of all names, all courses returned
    courses = Course.get_courses_ordered_by_name("")
    assert isinstance(courses, QuerySet)
    assert all(isinstance(course, Course) for course in courses)


@pytest.mark.parametrize("course_name_exist, expected_output", [
    ("Resonance", ["Resonance in Runes and Signs"]),
    ("Numer", ["Numerology"]),
    ("in", ["Grammatica in Arithmancy", "Resonance in Runes and Signs", "UnFogging the Future"]),
])
@pytest.mark.django_db
def test_name_exists_get_courses_ordered_by_name(course_name_exist, expected_output):
    courses = Course.get_courses_ordered_by_name(course_name_exist)
    assert all(course.name in expected_output for course in courses)


@pytest.mark.parametrize("wrong_course_name", [
    ("Introduction to Poetry"),
    ("Introduction to Buddhism"),
])
@pytest.mark.django_db
def test_wrong_name_get_courses_ordered_by_name(wrong_course_name):
    courses = Course.get_courses_ordered_by_name(wrong_course_name)
    assert not courses


@pytest.mark.django_db
def test_lexicography_order_get_courses_ordered_by_name():
    courses = list(Course.get_courses_ordered_by_name(""))
    for index in range(len(courses)-1):
        assert courses[index].name < courses[index+1].name


# --------Front End testing-------- #
@pytest.fixture
def sign_in(client):
    client.post('/users/sign_in/', data={'username': 'testUser1', 'password': 'password123'})


@pytest.mark.django_db
@pytest.mark.usefixtures("sign_in")
def test_renders_add_review_search_template(client):
    response = client.get('/add_review_search/')
    assert response.status_code == 200
    assertTemplateUsed(response, 'homepage/add_review_search.html')


@pytest.mark.django_db
@pytest.mark.usefixtures("sign_in")
def test_get_course_by_name_with_client(client):
    response = client.get('/add_review_search/', {'course': 'Resonance'})
    courses_not_found = [b'Grammatica in Arithmancy', b'Numerology', b'UnFogging the Future']
    assert response.status_code == 200
    assert b'Resonance' in response.content
    assert all(course not in response.content for course in courses_not_found)


@pytest.mark.django_db
@pytest.mark.usefixtures("sign_in")
def test_wrong_course_name_with_client(client):
    response = client.get('/add_review_search/', {'course': 'Introduction to Buddhism'})
    assert response.status_code == 200


@pytest.mark.django_db
def test_redirect_unsigned_user_to_sign_in_page(client):
    response = client.get('/add_review_search/', {'course': 'UnFogging the Future'})
    assert response.status_code == 302
    assert '/users/sign_in/' in response.url
