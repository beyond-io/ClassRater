import pytest
from homepage.models import AppUser


@pytest.mark.django_db
class TestAppUser:

    @pytest.fixture
    def test_appUsers(self):
        appUser1 = AppUser.create_appUser('user1', 'user1@mta.ac.il', 'useruser222')
        appUser2 = AppUser.create_appUser('user2', 'user2@mta.ac.il', '1234')
        appUser3 = AppUser.create_appUser('user3', 'user3@gmail.com', '10101010')

        return (appUser1, appUser2, appUser3)

    def test_create_appUser(self, test_appUsers):
        assert isinstance(test_appUsers[0], AppUser)

        all_AppUsers = AppUser.get_all_appUsers()
        assert test_appUsers[0] in all_AppUsers

    def test_toggle_user_activation(self, test_appUsers):
        assert test_appUsers[0].user.is_active is True

        test_appUsers[0].toggle_user_activation()
        assert test_appUsers[0].user.is_active is False

        test_appUsers[0].toggle_user_activation()
        assert test_appUsers[0].user.is_active is True

    def test_get_all_appUsers(self, test_appUsers):
        all_AppUsers = AppUser.get_all_appUsers()
        assert (test_appUsers[0] in all_AppUsers
                and test_appUsers[1] in all_AppUsers
                and test_appUsers[2] in all_AppUsers)

    def test_find_appUser(self, test_appUsers):
        assert (AppUser.find_appUser('user1')
                and AppUser.find_appUser('user2')
                and AppUser.find_appUser('user3'))

        assert not AppUser.find_appUser('unknown_user')
