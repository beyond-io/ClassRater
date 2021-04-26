import pytest
from homepage.models import AppUser


@pytest.mark.django_db
class TestAppUser:

    @pytest.fixture
    def appUsers(self):
        appUser1 = AppUser.create_appUser('user1', 'user1@mta.ac.il', 'useruser222')
        appUser2 = AppUser.create_appUser('user2', 'user2@mta.ac.il', '1234')
        appUser3 = AppUser.create_appUser('user3', 'user3@gmail.com', '10101010')

        return (appUser1, appUser2, appUser3)

    # This method tests:
    # 1. The appUser created is the correct type of object (AppUser)
    # 2. The appUser was created sucesfully and saved in the DB
    def test_create_appUser(self, appUsers):
        assert isinstance(appUsers[0], AppUser)
        assert AppUser.objects.filter(pk = appUsers[0].pk).exists()

    def test_toggle_user_activation(self, appUsers):
        assert appUsers[0].user.is_active is True

        appUsers[0].toggle_user_activation()
        assert appUsers[0].user.is_active is False

        appUsers[0].toggle_user_activation()
        assert appUsers[0].user.is_active is True

    def test_get_all_appUsers(self, appUsers):
        all_AppUsers = AppUser.get_all_appUsers()
        assert (appUsers[0] in all_AppUsers
                and appUsers[1] in all_AppUsers
                and appUsers[2] in all_AppUsers)

    def test_find_appUser(self, appUsers):
        assert (AppUser.find_appUser('user1')
                and AppUser.find_appUser('user2')
                and AppUser.find_appUser('user3'))

        assert AppUser.find_appUser('unknown_user') == None
