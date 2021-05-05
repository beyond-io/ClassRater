import pytest
from homepage.forms import SignUpForm
from django.contrib.auth.models import User
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
class TestSignUp:

    @pytest.fixture
    def valid_user_details(self):
        return {
            'username': 'valid_username', 'email': 'valid@email.com', 'password1': 'pw123123', 'password2': 'pw123123'}

    @pytest.mark.parametrize("invalid_user_details", [
        # username cannot be None
        {'username': None, 'email': 'valid@email.com', 'password1': 'pw123123', 'password2': 'pw123123'},
        # email cannot be None
        {'username': 'valid_username', None: 'valid@email.com', 'password1': 'pw123123', 'password2': 'pw123123'},
        # password cannot be None
        {'username': 'valid_username', 'email': 'valid@email.com', 'password1': None, 'password2': None},
        # passowrds do not match
        {'username': 'valid_username', 'email': 'valid@email.com', 'password1': '000000000', 'password2': 'pw123123'}
    ])
    # ------------------------Back-End testing------------------------ #
    def test_signup_invalid(self, invalid_user_details):
        invalid = False
        form = SignUpForm(data=invalid_user_details)

        try:
            form.save()
        except ValueError:
            invalid = True

        assert invalid

    def test_signup_valid(self, valid_user_details):
        form = SignUpForm(data=valid_user_details)

        if form.is_valid():
            user = form.save()
            assert User.objects.filter(pk=user.id).exists()
        else:
            assert False

    # ------------------------Front-End testing------------------------ #

    def test_uses_signup_form(self, client):
        response = client.get('/users/sign_up/')

        assert response.status_code == 200
        assert isinstance(response.context['form'], SignUpForm)

    def test_post_valid_signup_with_client(self, client, valid_user_details):
        response = client.post('/users/sign_up/', data=valid_user_details)
        assert response.status_code == 302

    def test_renders_add_signup_template(self, client):
        response = client.get('/users/sign_up/')

        assert response.status_code == 200
        assertTemplateUsed(response, 'homepage/users/sign_up.html')
