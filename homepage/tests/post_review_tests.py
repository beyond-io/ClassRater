import pytest
from homepage.forms import ReviewForm
from homepage.models import Review
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
    form = ReviewForm(data=invalid_review_details)

    try:
        form.save()
    except ValueError:
        invalid = True

    assert invalid


@pytest.mark.django_db
def test_post_valid_review(review_details):
    form = ReviewForm(data=review_details)

    if form.is_valid():
        review = form.save()
        assert Review.objects.filter(pk=review.id).exists()
    else:
        assert False


# --------Front End testing-------- #
@pytest.mark.django_db
def test_uses_review_form(client):
    response = client.get('/add_review/')

    assert response.status_code == 200
    assert isinstance(response.context['form'], ReviewForm)


@pytest.mark.django_db
def test_post_valid_review_with_client(client, review_details):
    response = client.post('/add_review/', data=review_details)

    assert response.status_code == 302


@pytest.mark.django_db
def test_renders_add_review_template(client):
    response = client.get('/add_review/')

    assert response.status_code == 200
    assertTemplateUsed(response, 'homepage/add_review.html')
