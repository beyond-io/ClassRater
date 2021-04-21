import pytest
from homepage.models import AppUser, FollowedUserCourses, Course


@pytest.mark.django_db
class TestFollowedUserCourses:

    def test_get_courses_followed_by_appUser(self):
        appUser1 = AppUser.create_appUser('user1', 'user1@mta.ac.il', '1234')
        appUser2 = AppUser.create_appUser('user2', 'user2@gmail.com', '1234')
        appUser_noCourses = AppUser.create_appUser('user3', 'user3@', '9722')

        course1 = Course(course_id=10231, name='course1', mandatory=True, credit_points=0, avg_load=0,
                         avg_rating=0, num_of_raters=0, num_of_reviewers=0)
        course1.save()

        course2 = Course(course_id=10400, name='course2', mandatory=True, credit_points=0,
                         avg_load=0, avg_rating=0, num_of_raters=0, num_of_reviewers=0)
        course2.save()

        user_course_pair_1 = FollowedUserCourses(user=appUser1, course=course1)
        user_course_pair_1.save()
        user_course_pair_2 = FollowedUserCourses(user=appUser1, course=course2)
        user_course_pair_2.save()
        user_course_pair_3 = FollowedUserCourses(user=appUser2, course=course2)
        user_course_pair_3.save()

        appUser1_followed_courses = FollowedUserCourses.get_courses_followed_by_appUser(appUser1)
        appUser2_followed_courses = FollowedUserCourses.get_courses_followed_by_appUser(appUser2)
        appUser_noCourses_followed_courses = FollowedUserCourses.get_courses_followed_by_appUser(appUser_noCourses)

        assert (course1 in appUser1_followed_courses) and (course2 in appUser1_followed_courses)
        assert course2 in appUser2_followed_courses
        assert course1 not in appUser2_followed_courses
        assert appUser_noCourses_followed_courses == []
