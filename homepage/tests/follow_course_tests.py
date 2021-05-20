import pytest
from homepage.models import Course, FollowedUserCourses
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestMyProfile:

    @pytest.fixture
    def followed_course_pair(self):
        user = User.objects.get(username='testUser1')
        course = Course.objects.get(name='Grammatica in Arithmancy')
        return (user, course)

    @pytest.fixture
    def not_followed_pair(self):
        user = User.objects.get(username='testUser1')
        course = Course.objects.get(name='Numerology')
        return (user, course)

    @pytest.fixture
    def signed_up_user_details(self):
        return {'username': 'testUser1', 'password': 'password123'}

    @pytest.fixture
    def signed_in(self, client, signed_up_user_details):
        return client.post('/users/sign_in/', data=signed_up_user_details)

    # ----------------------------------------------------------------------------------------------- #
    # Backend tests #

    def test_is_following_course(self, followed_course_pair):
        assert FollowedUserCourses.is_following_course(followed_course_pair[0], followed_course_pair[1])

    def test_follow_course(self, not_followed_pair):
        FollowedUserCourses.follow_course(not_followed_pair[0], not_followed_pair[1])
        assert FollowedUserCourses.is_following_course(not_followed_pair[0], not_followed_pair[1])

    def test_unfollow_course(self, followed_course_pair):
        FollowedUserCourses.unfollow_course(followed_course_pair[0], followed_course_pair[1])
        assert not FollowedUserCourses.is_following_course(followed_course_pair[0], followed_course_pair[1])

    # ----------------------------------------------------------------------------------------------- #
    # Frontend tests #

    def test_signed_in_follow_course(self, client, signed_in, followed_course_pair):
        # testUser1 unfollows the course Grammatica in Arithmancy
        FollowedUserCourses.unfollow_course(signed_in.wsgi_request.user, followed_course_pair[1])

        # after clicking on follow course button --> check that the user is following the course
        client.get('/course/10221/follow_course_action')
        assert FollowedUserCourses.is_following_course(signed_in.wsgi_request.user, followed_course_pair[1])

    def test_signed_in_unfollow_course(self, client, signed_in, followed_course_pair):
        # testUser1 follows the course Grammatica in Arithmancy
        FollowedUserCourses.follow_course(signed_in.wsgi_request.user, followed_course_pair[1])

        # after clicking the button --> check that the user is not following the course
        client.get('/course/10221/follow_course_action')
        assert not FollowedUserCourses.is_following_course(signed_in.wsgi_request.user, followed_course_pair[1])

    def test_signed_in_follow_course_action_redirect(self, client, signed_in):
        response = client.get('/course/10340/follow_course_action')
        assert response.url == ('/course/10340/')

    def test_signed_in_follow_course_invalid_url_redirect(self, client, signed_in):
        response = client.get('/course/00000/follow_course_action')
        assert response.url == ('/courses/')

    def test_signed_out_follow_course_action_redirect(self, client):
        client.post('/users/sign_out/')
        response = client.get('/course/10340/follow_course_action')
        assert response.url == ('/users/sign_in/?next=/course/10340/follow_course_action')
