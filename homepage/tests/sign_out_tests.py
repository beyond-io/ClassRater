import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestSignOut:

    @pytest.fixture
    def sign_in_user(self, client):
        User.objects.create_user(username='valid_username', email='valid@email.com', password='pw123123')
        client.post('/users/sign_in/', data={'username': 'valid_username2', 'password': 'pw123123'})

    def test_sign_out_user_with_client(self, client, sign_in_user):
        response = client.post('/users/sign_out/')
        assert not response.wsgi_request.user.is_authenticated

    def test_sign_out_redirect(self, client):
        response = client.get('/users/sign_out/')
        HOMEPAGE_URL = '/'
        assert response.url == HOMEPAGE_URL
