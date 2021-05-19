import pytest
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
class TestMyProfile:

    @pytest.fixture
    def signed_up_user_details(self):
        return {'username': 'testUser1', 'password': 'password123'}

    def test_user_renders_profile_template(self, client, signed_up_user_details):
        # log in with testUser1 using the sign-in page to acesss his profile
        client.post('/users/sign_in/', data=signed_up_user_details)

        response = client.get('/users/my_profile/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'homepage/users/my_profile.html')

    # AnonymousUser is Django's request.user when no user is currently logged in
    def test_anonymous_user_accesses_my_profile(self, client):
        response = client.get('/users/my_profile/')
        assert response.url == ('/users/sign_in/?next=/users/my_profile/')
