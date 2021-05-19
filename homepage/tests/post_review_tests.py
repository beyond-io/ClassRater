import pytest
from homepage.forms import ReviewForm
from homepage.models import Review, Professor_to_Course
from pytest_django.asserts import assertTemplateUsed


@pytest.fixture
def review_details():
    return {'course': 10231, 'user': 3, 'rate': 5, 'content': "Great course!", 'course_load': 4, 'Professor': ''}


# --------Backend testing-------- #
@pytest.mark.parametrize("invalid_review_details", [
    {'course': 10231, 'user': 3, 'rate': 10, 'content': "Great course!", 'course_load': 4, 'Professor': None},
    # review_details0:                   ^rate > 5
    {'course': 10231, 'user': 3, 'rate': 4, 'content': "Great course!", 'course_load': -2, 'Professor': None},
    # review_details1:                                                                 ^course_load < 0
    {'course': 10231, 'user': '', 'rate': 4, 'content': "Great course!", 'course_load': -2, 'Professor': None},
    # review_details2:        ^user field is required
])
@pytest.mark.django_db
def test_post_invalid_review(invalid_review_details):
    invalid = False
    form = ReviewForm(data=invalid_review_details, user=invalid_review_details.get('user'),
                      course=invalid_review_details.get('course'))
    try:
        form.save()
    except ValueError:
        invalid = True
    assert invalid


@pytest.mark.django_db
def test_post_valid_review(review_details):
    form = ReviewForm(data=review_details, user=review_details.get('user'), course=review_details.get('course'))
    if form.is_valid():
        review = form.save()
        assert Review.objects.filter(pk=review.id).exists()
    else:
        assert False


@pytest.mark.parametrize("course_id, prof_id_list", [
    (10221, [1]),  # Grammatica in Arithmancy, Septima Vector
    (12357, [1]),  # Numerology, Septima Vector
    (10231, [2]),  # UnFogging the Future, Sybill Patricia Trelawney
    (10111, [3]),  # Resonance in Runes and Signs, Bathsheda Babbling
])
@pytest.mark.django_db
def test_get_queryset_professors_by_course(course_id, prof_id_list):
    professor_queryset = Professor_to_Course.get_queryset_professors_by_course(course_id)
    assert all(professor.id in prof_id_list for professor in professor_queryset)


@pytest.mark.parametrize("user_id, course_id, expected_result", [
    (1, 10111, True),
    (3, 10231, True),
    (1, 10231, False),
])
@pytest.mark.django_db
def test_user_already_posted_review(user_id, course_id, expected_result):
    assert Review.user_already_posted_review(user_id, course_id) == expected_result


# --------Front End testing-------- #
@pytest.fixture
def sign_in(client):
    client.post('/users/sign_in/', data={'username': 'testUser1', 'password': 'password123'})


@pytest.mark.django_db
@pytest.mark.usefixtures("sign_in")
def test_uses_review_form(client, review_details):
    course_id = review_details.get('course')
    response = client.get(f'/add_review/{course_id}')
    assert response.status_code == 200
    assert isinstance(response.context['form'], ReviewForm)


@pytest.mark.django_db
@pytest.mark.usefixtures("sign_in")
def test_post_valid_review_with_client(client, review_details):
    course_id = review_details.get('course')
    response = client.post(f'/add_review/{course_id}', data=review_details)
    assert response.status_code == 302
    assert response.url == f'/course/{course_id}/'


@pytest.mark.django_db
@pytest.mark.usefixtures("sign_in")
def test_renders_add_review_template(client, review_details):
    course_id = review_details.get('course')
    response = client.get(f'/add_review/{course_id}')
    assert response.status_code == 200
    assertTemplateUsed(response, 'homepage/add_review.html')


@pytest.mark.parametrize("course_id, excpected_status_code", [
    (10231, 200), (10221, 200), (12357, 200), (666, 302),
])
@pytest.mark.django_db
@pytest.mark.usefixtures("sign_in")
def test_add_review_request(client, course_id, excpected_status_code):
    response = client.get(f'/add_review/{course_id}')
    assert response.status_code == excpected_status_code


@pytest.mark.django_db
@pytest.mark.usefixtures("sign_in")
def test_user_already_posted_review_with_client(client):
    course_id = 10111
    response = client.get(f'/add_review/{course_id}')
    assert response.status_code == 302
    assert response.url == f'/course/{course_id}/'


@pytest.mark.django_db
def test_redirect_unsigned_user_to_sign_in_page(client):
    response = client.get('/add_review/10221')
    assert response.status_code == 302
    assert '/users/sign_in/' in response.url
