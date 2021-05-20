import pytest
from homepage.models import User, Review, UserLikes, Course
from pytest_django.asserts import assertTemplateUsed

@pytest.mark.django_db
@pytest.fixture
def db_data():
    return User.objects.get(pk=2), Review.objects.get(pk=5)

# check db when using view from reviews page
@pytest.mark.django_db
def test_view_toggle_like_from_reviews(client, db_data):
    likes_num_before = db_data[1].likes_num
    response = client.get(f'/like/{db_data[0].id}/{db_data[1].id}/', HTTP_REFERER='/reviews/')
    assert UserLikes.objects.filter(user_id=db_data[0], review_id=db_data[1]).exists()
    review = Review.objects.get(pk=5)  # pull updated
    assert review.likes_num == likes_num_before + 1


# check db when using view from single course page
@pytest.mark.django_db
def test_view_toggle_like_from_course(client, db_data):
    likes_num_before = db_data[1].likes_num
    response = client.get(f'/like/{db_data[0].id}/{db_data[1].id}/', HTTP_REFERER='/course/10111/')
    assert UserLikes.objects.filter(user_id=db_data[0], review_id=db_data[1]).exists()
    review = Review.objects.get(pk=5)  # pull updated
    assert review.likes_num == likes_num_before + 1


# check db when using invalid user id from valid reviews page
@pytest.mark.django_db
def test_view_toggle_like_invalid_user(client, db_data):
    likes_num_before = db_data[1].likes_num
    response = client.get(f'/like/10/3/', HTTP_REFERER='/reviews/')  # valid referrer
    assert not UserLikes.objects.filter(user_id=db_data[0], review_id=db_data[1]).exists()
    review = db_data[1]
    assert review.likes_num == likes_num_before


# check db when using invalid review id from valid reviews page
@pytest.mark.django_db
def test_view_toggle_like_invalid_review(client, db_data):
    likes_num_before = db_data[1].likes_num
    response = client.get(f'/like/3/30/', HTTP_REFERER='/reviews/')  # valid referrer
    assert not UserLikes.objects.filter(user_id=db_data[0], review_id=db_data[1]).exists()
    review = db_data[1]
    assert review.likes_num == likes_num_before


# check that it stays on the same page - reviews
@pytest.mark.django_db
def test_rendering_toggle_like_from_reviews(client):
    response = client.get(f'/like/2/5/', HTTP_REFERER='/reviews/')
    assert response.status_code == 302
    response = client.get(response.url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'homepage/reviews/reviews.html')


# check that it stays on the same page - single course
@pytest.mark.django_db
def test_rendering_toggle_like_from_course(client):
    response = client.get(f'/like/2/5/', HTTP_REFERER='/course/10111/')
    assert response.status_code == 302
    response = client.get(response.url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'homepage/courses/course.html')


# check page redirection without referrer header int the request
@pytest.mark.django_db
def test_rendering_toggle_like_without_referrer(client):
    response = client.get(f'/like/2/5/')
    assert response.status_code == 302
    response = client.get(response.url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'homepage/landing/landing.html')


# check page redirection when invalid user is given
@pytest.mark.django_db
def test_rendering_toggle_like_invalid_user(client):
    response = client.get(f'/like/10/5/', HTTP_REFERER='/reviews/')  # valid referrer
    assert response.status_code == 302
    response = client.get(response.url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'homepage/landing/landing.html')


# check page redirection when invalid review is given
@pytest.mark.django_db
def test_rendering_toggle_like_invalid_review(client):
    response = client.get(f'/like/3/30/', HTTP_REFERER='/reviews/')  # valid referrer
    assert response.status_code == 302
    response = client.get(response.url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'homepage/landing/landing.html')
