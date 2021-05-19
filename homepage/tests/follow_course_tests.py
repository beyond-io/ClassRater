import pytest
from homepage.models import Course, FollowedUserCourses
from django.contrib.auth.models import User


@pytest.mark.django_db
class FollowCourseActionTests:

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

    def test_is_following_course(self, followed_course_pair):
        assert FollowedUserCourses.is_following_course(followed_course_pair[0], followed_course_pair[1])

    def test_follow_course(self, not_followed_pair):
        FollowedUserCourses.follow_course(not_followed_pair[0], not_followed_pair[1])
        assert FollowedUserCourses.is_following_course(not_followed_pair[0], not_followed_pair[1])

    def test_un_follow_course(self, followed_course_pair):
        FollowedUserCourses.un_follow_course(followed_course_pair[0], followed_course_pair[1])
        assert not FollowedUserCourses.is_following_course(followed_course_pair[0], followed_course_pair[1])

    def test_follow_course_redirect(self, client):
        response = client.get('/course/10340/follow_course_action')
        assert response.url == ('/course/10340/')
