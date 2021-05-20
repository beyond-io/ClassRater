import pytest
from homepage.models import User, Review, UserLikes
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
@pytest.fixture
def db_data():
    return User.objects.get(pk=2), Review.objects.get(pk=5)


# check db when using view from a valid page
@pytest.mark.parametrize("valid_referrer", [
    ('/reviews/'),
    ('/course/10111/'),
])
@pytest.mark.django_db
def test_view_toggle_like_from_with_valid_referrers(client, db_data, valid_referrer):
    likes_num_before = db_data[1].likes_num
    client.get(f'/like/{db_data[0].id}/{db_data[1].id}/', HTTP_REFERER=valid_referrer)
    assert UserLikes.objects.filter(user_id=db_data[0], review_id=db_data[1]).exists()
    review = Review.objects.get(pk=5)  # pull updated
    assert review.likes_num == likes_num_before + 1


# check db when using invalid user data from a valid page
@pytest.mark.parametrize("invalid_data_path", [
    ('/like/10/3/'),  # invalid user id
    ('/like/3/30/'),  # invalid review id
])
@pytest.mark.django_db
def test_view_toggle_like_invalid_data_in_path(client, db_data, invalid_data_path):
    likes_num_before = db_data[1].likes_num
    client.get(invalid_data_path, HTTP_REFERER='/reviews/')  # valid referrer
    assert not UserLikes.objects.filter(user_id=db_data[0], review_id=db_data[1]).exists()
    review = db_data[1]
    assert review.likes_num == likes_num_before


# check that it stays on the same page
@pytest.mark.parametrize("valid_referrer, valid_template", [
    ('/reviews/', 'homepage/reviews/reviews.html'),  # invalid user id
    ('/course/10111/', 'homepage/courses/course.html'),  # invalid review id
])
@pytest.mark.django_db
def test_rendering_toggle_like_from_valid_referrers(client, valid_referrer, valid_template):
    response = client.get('/like/2/5/', HTTP_REFERER=valid_referrer)
    assert response.status_code == 302
    response = client.get(response.url)
    assert response.status_code == 200
    assertTemplateUsed(response, valid_template)


# check page redirection without referrer header in the request
@pytest.mark.django_db
def test_rendering_toggle_like_without_referrer(client):
    response = client.get('/like/2/5/')
    assert response.status_code == 302
    response = client.get(response.url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'homepage/landing/landing.html')


# check page redirection when invalid data is given
@pytest.mark.parametrize("invalid_data_path", [
    ('/like/10/3/'),  # invalid user id
    ('/like/3/30/'),  # invalid review id
])
@pytest.mark.django_db
def test_rendering_toggle_like_invalid_data_in_path(client, invalid_data_path):
    response = client.get(invalid_data_path, HTTP_REFERER='/reviews/')  # valid referrer
    assert response.status_code == 302
    response = client.get(response.url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'homepage/landing/landing.html')
