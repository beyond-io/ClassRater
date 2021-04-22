import pytest
from homepage.models import AppUser, FollowedUserCourses, Course


@pytest.mark.django_db
class TestAppUser:

    def test_create_appUser(self):
        appUser = AppUser.create_appUser('Jhon1', 'Jhon1@mta.ac.il', '1234')

        # check that appUser is the correct type of Object
        assert isinstance(appUser, AppUser)

        # check that appUser was sucesfully saved in the DB
        all_AppUsers = AppUser.get_all_appUsers()
        assert appUser in all_AppUsers

    def test_toggle_user_activation(self):
        appUser = AppUser.create_appUser('Jhon2', 'Jhon2@mta.ac.il', '1234')

        appUser.toggle_user_activation()
        assert appUser.user.is_active is False

        appUser.toggle_user_activation()
        assert appUser.user.is_active is True

    def test_get_all_appUsers(self):
        appUser1 = AppUser.create_appUser('Jhon3', 'Jhon3@mta.ac.il', '1234')
        appUser2 = AppUser.create_appUser('Jhon4', 'Jhon4@mta.ac.il', '1234')
        appUser3 = AppUser.create_appUser('Jhon5', 'Jhon5@mta.ac.il', '1234')

        all_AppUsers = AppUser.get_all_appUsers()
        assert (appUser1 in all_AppUsers) and (appUser2 in all_AppUsers) and (appUser3 in all_AppUsers)

    def test_find_appUser(self):
        AppUser.create_appUser('Jhon6', 'Jhon6@mta.ac.il', '1234')
        AppUser.create_appUser('Jhon7', 'Jhon7@mta.ac.il', '1234')
        AppUser.create_appUser('Jhon8', 'Jhon8@mta.ac.il', '1234')

        assert AppUser.find_appUser('Jhon6') and AppUser.find_appUser('Jhon7') and AppUser.find_appUser('Jhon8')


@pytest.mark.django_db
class TestFollowedUserCourses:

    def test_get_courses_followed_by_appUser(self):
        appUser1 = AppUser.create_appUser('Jhon9', 'Jhon9@mta.ac.il', '1234')
        appUser2 = AppUser.create_appUser('Jhon10', 'Jhon10@mta.ac.il', '1234')

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

        assert (course1 in appUser1_followed_courses) and (course2 in appUser1_followed_courses)
        assert course2 in appUser2_followed_courses
