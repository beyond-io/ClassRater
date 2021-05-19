import pytest
from homepage.models import AppUser


@pytest.mark.django_db
class TestAppUser:

    @pytest.fixture
    def app_users(self):
        app_user1 = AppUser.create_app_user('user1', 'user1@mta.ac.il', 'useruser222')
        app_user2 = AppUser.create_app_user('user2', 'user2@mta.ac.il', '1234')
        app_user3 = AppUser.create_app_user('user3', 'user3@mta.ac.il', '10101010')
        return (app_user1, app_user2, app_user3)

    # The 3 appUsers created in the fixture above are:
    # 1. The correct type of object (AppUser)
    # 2. Successfully saved in the DB
    def test_create_app_user(self, app_users):
        for app_user in app_users:
            assert isinstance(app_user, AppUser)
            assert AppUser.objects.filter(pk=app_user.pk).exists()

    # An app_user with invalid username is not created
    def test_invald_username(self, app_users):
        try:
            AppUser.create_app_user('', 'user4@mta.ac.il', 'useruser222')
        except ValueError:
            invalid_username_created = False
        assert invalid_username_created is False

    # An app_user with empty password does not have a usuable password (Django built in create_user behaviour)
    def test_invalid_password(self, app_users):
        app_user_invalid_password = AppUser.create_app_user('user6', 'user6@mta.ac.il', None)
        assert (app_user_invalid_password.user).has_usable_password() is False

    def test_is_active_user(self, app_users):
        for app_user in app_users:
            assert app_user.user.is_active

    def test_toggle_user_activation(self, app_users):
        for app_user in app_users:
            app_user.toggle_user_activation()
            assert app_user.user.is_active is False

            app_user.toggle_user_activation()
            assert app_user.user.is_active

    def test_get_all_app_users(self, app_users):
        all_AppUsers = AppUser.get_all_app_users()
        for app_user in app_users:
            assert app_user in all_AppUsers

    def test_get_app_user(self, app_users):
        for app_user in app_users:
            assert AppUser.get_app_user(app_user.user.username)

    def test_get_undefined_app_user(self):
        assert AppUser.get_app_user('unknown_user') is None
