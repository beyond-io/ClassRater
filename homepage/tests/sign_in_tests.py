import pytest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
class TestSignIn:

    @pytest.fixture
    def signed_up_details(self):
        User.objects.create_user(username='valid_username', email='valid@email.com', password='pw123123')
        return ['valid_username', 'pw123123']

    @pytest.fixture
    def not_signed_up_details(self):
        return ['not_valid_username', 'pw123123']

    # ------------------------Back-End testing------------------------ #

    def test_signin_invalid(self, not_signed_up_details):
        user = authenticate(username=not_signed_up_details[0], password=not_signed_up_details[1])
        assert user is None

    def test_signin_valid(self, signed_up_details):
        user = authenticate(username=signed_up_details[0], password=signed_up_details[1])
        assert user

    # ------------------------Front-End testing------------------------ #

    def test_post_valid_signIn_with_client(self, client, signed_up_details):
        response = client.post('/users/sign_in/', data={
            'username': signed_up_details[0], 'password': signed_up_details[1]})

        HOMEPAGE_URL = '/'
        assert response.url == HOMEPAGE_URL
        assert response.status_code == 302

    def test_invalid_signIn_redirect(self, client, not_signed_up_details):
        response = client.post('/users/sign_in/', data={
            'username': not_signed_up_details[0], 'password': not_signed_up_details[1]})

        assert response.url == '/users/sign_in/'

    def test_renders_add_signIn_template(self, client):
        response = client.get('/users/sign_in/')

        assert response.status_code == 200
        assertTemplateUsed(response, 'homepage/users/sign_in.html')

    def test_uses_authenticate_form(self, client):
        response = client.get('/users/sign_in/')

        assert response.status_code == 200
        assert isinstance(response.context['form'], AuthenticationForm)
