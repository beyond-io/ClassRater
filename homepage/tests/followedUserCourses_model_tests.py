import pytest
from homepage.models import AppUser, Course, FollowedUserCourses


@pytest.mark.django_db
class TestFollowedUserCourses:

    # -----------------------------------------------#
    # create the test data (app_user, courses, user_course_pairs) that will be used in the test methods
    @pytest.fixture
    def app_users(self):
        app_user0 = AppUser.create_app_user('user0', 'user1@mta.ac.il', '1234')
        app_user1 = AppUser.create_app_user('user1', 'user2@gmail.com', '1234')
        app_user_notFollowing = AppUser.create_app_user('user_notFollowing', 'user3@', '9722')
        return (app_user0, app_user1, app_user_notFollowing)

    @pytest.fixture
    def courses(self):
        course0 = Course(course_id=100231, name='course0', mandatory=True, credit_points=1)
        course0.save()
        course1 = Course(course_id=100400, name='course1', mandatory=True, credit_points=1)
        course1.save()
        return (course0, course1)

    @pytest.fixture
    def create_user_course_pairs(self, app_users, courses):
        user0_course0 = FollowedUserCourses(user=app_users[0], course=courses[0]).save()
        user0_course1 = FollowedUserCourses(user=app_users[0], course=courses[1]).save()
        user1_course1 = FollowedUserCourses(user=app_users[1], course=courses[1]).save()
        return (user0_course0, user0_course1, user1_course1)

    # end of test data creation
    # -----------------------------------------------#

    # app_users[0] is following course[0], course[1]
    def test_get_courses_followed_by_app_user_0(self, app_users, courses, create_user_course_pairs):
        app_user0_courses = FollowedUserCourses.get_courses_followed_by_app_user(app_users[0])
        assert (courses[0] in app_user0_courses) and (courses[1] in app_user0_courses)

    # app_users[1] is following course[1], not following course[0]
    def test_get_courses_followed_by_app_user_1(self, app_users, courses, create_user_course_pairs):
        app_user1_courses = FollowedUserCourses.get_courses_followed_by_app_user(app_users[1])
        assert courses[1] in app_user1_courses
        assert courses[0] not in app_user1_courses

    # app_users[2] is not following any courses
    def test_get_courses_not_followed(self, app_users, courses, create_user_course_pairs):
        app_user2_courses = FollowedUserCourses.get_courses_followed_by_app_user(app_users[2])
        assert app_user2_courses == []
