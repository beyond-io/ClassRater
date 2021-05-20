import pytest
from homepage.models import Course, Prerequisites
from homepage.forms import FilterAndSortForm
from pytest_django.asserts import assertTemplateUsed
from decimal import Decimal


# --- testing the filtering functions:
@pytest.fixture
def courses():
    courses_list = [
         Course(1, "Course1", True, 3, None, 1.3, 4, 5, 1),
         Course(2, "Course2", False, 2, None, 3.5, 2, 13, 5),
         Course(3, "Course3", False, 1, None, 2, 2.5, 2, 0)
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


@pytest.mark.django_db
def test_get_courses_with_preq(all_courses):
    courses = Course.get_courses_with_preqs(all_courses)
    assert all(course.has_preqs() for course in courses)


@pytest.mark.django_db
def test_get_courses_without_preq(all_courses):
    courses = Course.get_courses_without_preqs(all_courses)
    assert all(not course.has_preqs() for course in courses)


@pytest.mark.django_db
def test_get_courses_with_ratings(all_courses):
    courses = Course.get_courses_with_ratings(all_courses, 5)
    assert all(course.num_of_raters >= 5 for course in courses)


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


# -- test the overreaching filter method - result and active parameters
@pytest.fixture
def filters_to_results(all_courses):
    return {
        'mand': Course.get_mandatory_courses(all_courses),
        'elect': Course.get_elective_courses(all_courses),
        'load_below': Course.get_filtered_courses_by_load(3.5, all_courses),
        'rate_over': Course.get_filtered_courses_by_rating(3.5, all_courses),
        'has_preqs': Course.get_courses_with_preqs(all_courses),
        'no_preqs': Course.get_courses_without_preqs(all_courses),
        'rater_num': Course.get_courses_with_ratings(all_courses, 5)
        }


@pytest.fixture
def filters_to_active():
    return {
        'mand': 'mandatory',
        'elect': 'elective',
        'load_below': 'course load under 3.5',
        'rate_over': 'course rating over 3.5',
        'has_preqs': 'with prerequisites',
        'no_preqs': 'without prerequisites',
        'rater_num': 'at least 5 raters'
        }


@pytest.mark.django_db
def test_get_filtered_courses_result(all_courses, filters_to_results):
    for key, val in filters_to_results.items():
        assert list(Course.get_filtered_courses(all_courses, [key])['result']) == list(val)


@pytest.mark.django_db
def test_get_filtered_courses_active_filters(all_courses, filters_to_active):
    for key, val in filters_to_active.items():
        assert Course.get_filtered_courses(all_courses, [key])['active'][0] == val


# --- sorting tests

@pytest.mark.django_db
def test_sort_by_name(all_courses):
    courses = list(Course.sort_by_name(all_courses))
    for index in range(len(courses)-1):
        assert courses[index].name < courses[index+1].name


@pytest.mark.django_db
def test_sort_by_id(all_courses):
    courses = list(Course.sort_by_id(all_courses))
    for index in range(len(courses)-1):
        assert courses[index].course_id < courses[index+1].course_id


@pytest.mark.django_db
def test_sort_by_rating(all_courses):
    courses = list(Course.sort_by_rating(all_courses))
    for index in range(len(courses)-1):
        if courses[index].avg_rating is None:
            assert courses[index+1].avg_rating is None
        elif courses[index+1].avg_rating is not None:
            assert Decimal.compare(courses[index].avg_rating, courses[index+1].avg_rating) > -1


@pytest.mark.django_db
def test_sort_by_load(all_courses):
    courses = list(Course.sort_by_load(all_courses))
    for index in range(len(courses)-1):
        if courses[index].avg_load is not None:
            assert Decimal.compare(courses[index].avg_load, courses[index+1].avg_load) < 1


@pytest.mark.django_db
def test_sort_by_num_reviews(all_courses):
    courses = list(Course.sort_by_num_reviews(all_courses))
    for index in range(len(courses)-1):
        assert courses[index].num_of_reviewers >= courses[index+1].num_of_reviewers


@pytest.mark.django_db
def test_sort_by_num_raters(all_courses):
    courses = list(Course.sort_by_num_raters(all_courses))
    for index in range(len(courses)-1):
        assert courses[index].num_of_raters >= courses[index+1].num_of_raters


# --- test the overreaching sort method - result abd active parameters
@pytest.fixture
def sort_to_result(all_courses):
    return {
        'name': Course.sort_by_name(all_courses),
        'id': Course.sort_by_id(all_courses),
        'rating': Course.sort_by_rating(all_courses),
        'load': Course.sort_by_load(all_courses),
        'num_reviews': Course.sort_by_num_reviews(all_courses),
        'num_raters': Course.sort_by_num_raters(all_courses)
        }


@pytest.fixture
def sort_to_active():
    return {
        'name': 'name',
        'id': 'identifier',
        'rating': 'course rating',
        'load': 'course load',
        'num_reviews': 'number of reviews',
        'num_raters': 'number of raters'
        }


@pytest.mark.django_db
def test_get_sorted_courses_results(all_courses, sort_to_result):
    for key, val in sort_to_result.items():
        assert list(Course.get_sorted_courses(all_courses, key)['result']) == list(val)


@pytest.mark.django_db
def test_get_sorted_courses_active(all_courses, sort_to_active):
    for key, val in sort_to_active.items():
        assert Course.get_sorted_courses(all_courses, key)['active'] == val


# --- test the view and form --- #


# test that initial, no filter, sorted by course_id : QuerySet contains all courses from test_data in correct order
@pytest.mark.django_db
def test_with_client(client, all_courses):
    courses = list(all_courses.order_by('course_id').values_list('course_id'))
    response = client.get('/courses/')
    assert response.status_code == 200
    view_courses = list(response.context['all_courses'].values_list('course_id'))
    assert courses == view_courses


# test that the get response is the desired form model
@pytest.mark.django_db
def test_uses_filter_and_sort_form(client):
    response = client.get('/courses/')
    assert isinstance(response.context['form'], FilterAndSortForm)


# test that invalid filter gives all the courses:
@pytest.mark.django_db
def test_invalid_filter_with_client(all_courses, client):
    response = client.get('/courses/', data={'filter_by': 'choice', 'sort_by': 'id'})
    assert response.status_code == 200
    assert list(response.context['all_courses']) == list(all_courses)


# test that the form model reacts to valid input
@pytest.mark.parametrize("valid_filters", [
    'mand',
    'elect',
    'has_preqs',
    'no_preqs',
    'rate_over',
    'load_below',
    'rater_num'
    ])
@pytest.mark.django_db
def test_filter_result_with_client(client, valid_filters, filters_to_results):
    response = client.get('/courses/', data={'filter_by': valid_filters, 'sort_by': 'id'})
    assert response.status_code == 200
    assert list(response.context['all_courses']) == list(filters_to_results[valid_filters])


@pytest.mark.parametrize("valid_filters", [
    'mand',
    'elect',
    'has_preqs',
    'no_preqs',
    'rate_over',
    'load_below',
    'rater_num'
    ])
@pytest.mark.django_db
def test_filter_active_with_client(client, valid_filters, filters_to_active):
    response = client.get('/courses/', data={'filter_by': valid_filters, 'sort_by': 'id'})
    assert response.status_code == 200
    assert response.context['filters'].count(filters_to_active[valid_filters]) == 1


# test that invalid sort gives all courses ordered by id
@pytest.mark.django_db
def test_invalid_sort_with_client(client, sort_to_result):
    response = client.get('/courses/', data={'filter_by': 'no_preqs', 'sort_by': 'hoho'})
    assert response.status_code == 200
    assert list(response.context['all_courses']) == list(sort_to_result['id'])


# test that the form reacts well to valid sort input
@pytest.mark.parametrize("valid_sort", [
    'id',
    'name',
    'rating',
    'load',
    'num_reviews',
    'num_raters'
    ])
@pytest.mark.django_db
def test_sorting_result_with_client(client, sort_to_result, valid_sort):
    response = client.get('/courses/', data={'sort_by': valid_sort})
    assert response.status_code == 200
    assert list(response.context['all_courses']) == list(sort_to_result[valid_sort])


@pytest.mark.parametrize("valid_sort", [
    'id',
    'name',
    'rating',
    'load',
    'num_reviews',
    'num_raters'
    ])
@pytest.mark.django_db
def test_sorting_active_with_client(client, sort_to_active, valid_sort):
    response = client.get('/courses/', data={'sort_by': valid_sort})
    assert response.status_code == 200
    assert response.context['sort'] == sort_to_active[valid_sort]


# check correct template
@pytest.mark.django_db
def test_renders_reviews_template(client):
    response = client.get('/courses/')
    assert response.status_code == 200
    assertTemplateUsed(response, 'homepage/courses/courses.html')
