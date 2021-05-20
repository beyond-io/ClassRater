import pytest
from pytest_django.asserts import assertTemplateUsed
from homepage.models import Review, FollowedUserCourses, AppUser


@pytest.mark.django_db
class TestMyProfile:

    @pytest.fixture
    def signed_up_user_details(self):
        return {'username': 'testUser1', 'password': 'password123'}

    @pytest.fixture
    def sign_in(self, client, signed_up_user_details):
        return client.post('/users/sign_in/', data=signed_up_user_details)

    @pytest.fixture
    def signed_in_app_user(self, sign_in):
        return AppUser.get_app_user(sign_in.wsgi_request.user.username)

    @pytest.fixture
    def user_profile_followed_courses(self, client, sign_in):
        response = client.get('/users/my_profile/')
        return response.context['user_followed_courses']

    @pytest.fixture
    def user_profile_reviews(self, client, sign_in):
        response = client.get('/users/my_profile/')
        return response.context['user_reviews']

# ----------------------------------------------------------------------------- #

    def test_user_renders_profile_template(self, client, sign_in):
        response = client.get('/users/my_profile/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'homepage/users/my_profile.html')

    # AnonymousUser is Django's request.user when no user is currently logged in
    def test_anonymous_user_accesses_my_profile(self, client):
        client.post('/users/sign_out/')
        response = client.get('/users/my_profile/')
        assert response.url == ('/users/sign_in/?next=/users/my_profile/')

    def test_profile_page_reviews(self, sign_in, user_profile_reviews):
        user_reviews = Review.profile_page_feed(sign_in.wsgi_request.user)
        assert all(review in user_profile_reviews for review in user_reviews)

    def test_profile_page_no_reviews(self, client, signed_in_app_user):
        # Delete all user reviews, then check that profile page has no reviews
        Review.objects.filter(user=signed_in_app_user).delete()
        assert not client.get('/users/my_profile/').context['user_reviews']

    def test_profile_page_followed_courses(self, user_profile_followed_courses, signed_in_app_user):
        followed_courses = FollowedUserCourses.get_courses_followed_by_app_user(signed_in_app_user)
        assert all(course in user_profile_followed_courses for course in followed_courses)

    def test_profile_page_no_followed_courses(self, client, signed_in_app_user):
        # Delete all user followed courses, then check that profile page has no reviews
        FollowedUserCourses.objects.filter(user=signed_in_app_user).delete()
        assert not client.get('/users/my_profile/').context['user_followed_courses']
